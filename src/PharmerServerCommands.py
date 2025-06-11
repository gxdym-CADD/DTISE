import json
from datetime import datetime
from threading import Lock

# Assuming the existence of these classes and functions
class FastCgiIO:
    def __init__(self):
        pass

    def <<(self, content):
        print(content)

class Cgicc:
    def getEnvironment(self):
        class Environment:
            def getRemoteAddr(self):
                return "remote_addr"
        return Environment()

    def getTagValues(self, tag):
        # Mock implementation
        if tag == "qid":
            return ["123"]
        elif tag == "key":
            return ["receptor_key"]
        elif tag == "receptor":
            return ["receptor_data"]
        elif tag == "subset":
            return ["subset_id"]
        return []

class WebQueryManager:
    def get(self, qid):
        # Mock implementation
        if qid == 123:
            return "query_object"
        return None

    def getJSONInfo(self):
        # Mock implementation
        return {"info": "data"}

    def getSingleJSON(self, id):
        # Mock implementation
        return {id: "subset_data"}

class WebQueryHandle:
    def __init__(self, query):
        self.query = query

    def __bool__(self):
        return self.query is not None

def cgiTagExists(CGI, tag):
    return len(CGI.getTagValues(tag)) > 0

def cgiGetInt(CGI, tag):
    return int(CGI.getTagValues(tag)[0])

def cgiGetString(CGI, tag):
    return CGI.getTagValues(tag)[0]

class SpinMutex:
    def __init__(self):
        self.lock = Lock()

    def lock(self):
        self.lock.acquire()

    def unlock(self):
        self.lock.release()

# Command class
class Command:
    def __init__(self, LOG, logmutex):
        self.LOG = LOG
        self.logmutex = logmutex

    def sendError(self, IO, CGI, msg):
        IO << HTTPPlainHeader()
        IO << json.dumps({"status": 0, "msg": msg})
        if self.LOG:
            with open(self.LOG, 'a') as f:
                t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"error {t} {CGI.getEnvironment().getRemoteAddr()} {msg}\n")
                f.write("error cgi\n")

    def sendAck(self, IO, msg):
        IO << HTTPPlainHeader()
        IO << msg

# QueryCommand class
class QueryCommand(Command):
    def __init__(self, LOG, logmutex, queries):
        super().__init__(LOG, logmutex)
        self.queries = queries

    def getQuery(self, CGI, IO):
        if not cgiTagExists(CGI, "qid"):
            self.sendError(IO, CGI, "Bad data request. No query id.")
            return WebQueryHandle(None)
        else:
            qid = cgiGetInt(CGI, "qid")
            if qid == 0:
                self.sendError(IO, CGI, "Bad data request. Invalid query id.")
                return WebQueryHandle(None)
            query = self.queries.get(qid)
            if not query:
                self.sendError(IO, CGI, "Bad data request. Query not found.")
                return WebQueryHandle(None)
            return WebQueryHandle(query)

# SetSubset class
class SetSubset(Command):
    def __init__(self, LOG, logmutex, queries):
        super().__init__(LOG, logmutex)
        self.queries = queries

    def execute(self, CGI, IO):
        key = cgiGetString(CGI, "key")
        subset_data = cgiGetString(CGI, "subset")
        IO << HTTPPlainHeader()
        if not key or not subset_data:
            self.sendError(IO, CGI, "Bad data request. Missing key or subset data.")
            return
        try:
            self.queries.setSubset(key, subset_data)
            IO << "saved"
        except Exception as e:
            self.sendError(IO, CGI, str(e))

# GetSubsets class
class GetSubsets(Command):
    def __init__(self, queries, LOG, logmutex):
        super().__init__(LOG, logmutex)
        self.queries = queries

    def execute(self, CGI, IO):
        IO << HTTPPlainHeader()
        if not cgiTagExists(CGI, "subset"):
            info = self.queries.getJSONInfo()
            IO << json.dumps(info)
        else:
            id = cgiGetString(CGI, "subset")
            info = self.queries.getSingleJSON(id)
            IO << json.dumps(info)

# StartQuery class
class StartQuery(Command):
    def __init__(self, LOG, logmutex, queries, logdirpath):
        super().__init__(LOG, logmutex)
        self.queries = queries
        self.logdirpath = logdirpath

    def execute(self, CGI, IO):
        query_data = cgiGetString(CGI, "query")
        IO << HTTPPlainHeader()
        if not query_data:
            self.sendError(IO, CGI, "Bad data request. Missing query data.")
            return
        try:
            qid = self.queries.startNewQuery(query_data)
            IO << f"started {qid}"
        except Exception as e:
            self.sendError(IO, CGI, str(e))

# Mock HTTPPlainHeader function
def HTTPPlainHeader():
    return "Content-Type: application/json\n\n"
class StartQuery(Command):
    def __init__(self, queries: WebQueryManager, l: FILE, lm: SpinMutex, ldp: Path, ph: Pharmas):
        super().__init__(l, lm)
        self.queries = queries
        self.logdirpath = ldp
        self.recmutex = lm
        self.pharmas = ph

    def execute(self, CGI: Cgicc, IO: FastCgiIO):
        from json import loads
        from os.path import exists, join
        from threading import Lock

        if not cgiTagExists(CGI, "json"):
            # no query
            self.sendError(IO, CGI, "Invalid query syntax. No query data.")
        else:
            try:
                root = loads(cgiGetString(CGI, "json"))
            except ValueError:
                self.sendError(IO, CGI, "Invalid query. Could not parse query data.")
                return

            # check for memoized receptor
            if "receptorid" in root:
                if not isinstance(root["receptor"], str) or len(root["receptor"]) == 0:
                    recstr = ""
                    rname = join(self.logdirpath, root["receptorid"])
                    with Lock():
                        if exists(rname):
                            with open(rname, 'r') as rec:
                                root["receptor"] = rec.read()

            totalMols = 0
            totalConfs = 0
            msg = ""
            oldqid = cgiGetInt(CGI, "oldqid")

            # DEBUG code - output queries
            if True:
                with Lock():
                    from datetime import datetime
                    t = datetime.now()
                    print(f"startq {t} {CGI.getEnvironment().getRemoteAddr()} {cgiGetString(CGI, 'json')}", file=self.LOG)
                    self.LOG.flush()

            if True:
                t = datetime.now()
                lastname = join(self.logdirpath, "lastq")
                with open(lastname, 'w') as last:
                    print(f"{t}\n{CGI.getEnvironment().getRemoteAddr()}\n{cgiGetString(CGI, 'json')}", file=last)

            qid = self.queries.add(self.pharmas, root,
                                   QueryParameters(root), oldqid, totalMols, totalConfs, msg)
            if qid == 0:  # invalid query
                self.sendError(IO, CGI, msg)
            else:
                # write log
                with Lock():
                    t = datetime.now()
                    print(f"query {t} {CGI.getEnvironment().getRemoteAddr()} {qid}", file=self.LOG)
                    if "receptorid" in root:
                        print(root["receptorid"], file=self.LOG)
                    self.LOG.flush()

                # output json with query id and size of database
                IO << HTTPPlainHeader()
                IO << f'{{"status": 1, "qid": {qid}, "numMols": {totalMols}, "numConfs": {totalConfs}}}'
import datetime
from typing import Dict, Optional

class CGIEnvironment:
    def getRemoteAddr(self) -> str:
        pass

class CGI:
    @staticmethod
    def getString(cgi: 'CGI', key: str) -> str:
        pass

    @staticmethod
    def getInt(cgi: 'CGI', key: str) -> int:
        pass

    @staticmethod
    def tagExists(cgi: 'CGI', key: str) -> bool:
        pass

class FastCgiIO:
    def __lshift__(self, value: str):
        print(value)

class QueryCommand:
    def __init__(self, l, lm, qs):
        self.LOG = l
        self.mutex = lm
        self.queries = qs

class CancelQuery(QueryCommand):
    def execute(self, CGI: 'CGI', IO: 'FastCgiIO'):
        oldqid = CGI.getInt(CGI, "oldqid")
        query = self.queries.get(oldqid)
        if query:
            query.cancel()
        self.queries.purgeOldQueries()
        IO << HTTPPlainHeader()
        IO << '{"status": 1}'

class CancelSmina(QueryCommand):
    def execute(self, CGI: 'CGI', IO: 'FastCgiIO'):
        qid = CGI.getInt(CGI, "qid")
        query = self.queries.get(qid)
        if query:
            query.cancelSmina()
        IO << HTTPPlainHeader()
        IO << '{"status": 1}'

class Ping(Command):
    def execute(self, CGI: 'CGI', IO: 'FastCgiIO'):
        IO << HTTPPlainHeader()

class GetData(QueryCommand):
    def initDataParams(self, data: 'CGI', params: 'DataParameters'):
        params.drawCode = data.getInt(data, "draw")
        params.start = data.getInt(data, "start")
        params.num = data.getInt(data, "length")
        params.sort = SortType[data.getInt(data, "order[0][column]")]  # Assuming SortType is an enum
        if data.getString(data, "order[0][dir]") == "desc":
            params.reverseSort = True
        params.extraInfo = True

    def execute(self, CGI: 'CGI', IO: 'FastCgiIO'):
        query = self.getQuery(CGI, IO)
        if query:
            IO << HTTPPlainHeader()
            params = DataParameters()
            self.initDataParams(CGI, params)
            val = Json::Value()
            query.setDataJSON(params, val)
            IO << val

    def isFrequent(self) -> bool:
        return True

class GetPharma(Command):
    def __init__(self, l: 'FILE', lm: 'SpinMutex', ph: 'Pharmas', p: Dict[str, 'QueryParser'], ldp: str):
        self.LOG = l
        self.mutex = lm
        self.pharmas = ph
        self.parsers = p
        self.logdirpath = ldp

    def execute(self, CGI: 'CGI', IO: 'FastCgiIO'):
        if not CGI.tagExists(CGI, "ligand") or not CGI.tagExists(CGI, "ligandname"):
            sendError(IO, CGI, "No ligand for pharmacophore identification.")
            return
        else:
            val = Json::Value()
            filedata = CGI.getString(CGI, "ligand")
            filename = CGI.getString(CGI, "ligandname")
            format = OBConversion.FormatFromExt(filename.encode())
            ext = os.path.splitext(filename)[1]
            if ext in self.parsers:
                # a pharmacophore query format
                str_stream = io.StringIO(filedata)
                points: List[PharmaPoint] = []
                excluder = ShapeConstraints()
from typing import List
import os
import io
from collections import defaultdict

class PharmaPoint:
    pass  # Define the PharmaPoint class as needed

class ShapeConstraints:
    def addToJSON(self, val):
        pass  # Implement addToJSON method

class OBFormat:
    pass  # Define the OBFormat class as needed

class OBConversion:
    @staticmethod
    def FormatFromExt(filename: str) -> OBFormat:
        pass  # Implement FormatFromExt method

class Cgicc:
    @staticmethod
    def getString(CGI, key: str) -> str:
        pass  # Implement getString method

    @staticmethod
    def getInt(CGI, key: str) -> int:
        pass  # Implement getInt method

    @staticmethod
    def getFiles() -> List['FormFile']:
        pass  # Implement getFiles method

class FormFile:
    def getData(self) -> str:
        pass  # Implement getData method

class FastCgiIO:
    def __init__(self):
        self.output = []

    def write(self, data: str):
        self.output.append(data)

    def __str__(self):
        return ''.join(self.output)

class WebQueryHandle:
    def outputMol(self, index: int, IO: FastCgiIO, minimize: bool):
        pass  # Implement outputMol method

    def numResults(self) -> int:
        pass  # Implement numResults method

    def outputMols(self, IO: FastCgiIO):
        pass  # Implement outputMols method

class QueryCommand:
    def __init__(self, l, lm, qs):
        self.l = l
        self.lm = lm
        self.qs = qs

    def getQuery(self, CGI, IO) -> WebQueryHandle:
        pass  # Implement getQuery method

class GetMol(QueryCommand):
    def execute(self, CGI: Cgicc, IO: FastCgiIO):
        query = self.getQuery(CGI, IO)
        if query:
            IO.write("HTTP/1.0 200 OK\n")
            index = CGI.getInt(CGI, "loc")
            query.outputMol(index, IO, False, CGI.getTagExists(CGI, "minimize"))

class SaveRes(QueryCommand):
    def execute(self, CGI: Cgicc, IO: FastCgiIO):
        from boost import SpinLock, posix_time
        query = self.getQuery(CGI, IO)
        if query:
            nR = query.numResults()
            lock = SpinLock(logmutex)
            t = posix_time.second_clock.local_time()
            print(f"save {posix_time.to_simple_string(t)} {CGI.getEnvironment().getRemoteHost()} {CGI.getInt(CGI, 'qid')} {nR}", file=LOG)
            lock.release()

            IO.write("Content-Type: text/sdf\n")
            IO.write("Content-Disposition: attachment; filename=query_results.sdf\n")
            IO.write("\n")
            query.outputMols(IO)

class Receptor(Command):
    def execute(self, CGI: Cgicc, IO: FastCgiIO):
        IO.write("HTTP/1.0 200 OK\n")
        IO.write("<html><body>\n")
        for f in CGI.getFiles():
            IO.write(f.getData())
        IO.write("</body></html>\n")

class Echo(Command):
    def execute(self, CGI: Cgicc, IO: FastCgiIO):
        pass  # Implement execute method

# Example usage
cgi = Cgicc()
io = FastCgiIO()

get_mol = GetMol(None, None, None)
get_mol.execute(cgi, io)

save_res = SaveRes(None, None, None)
save_res.execute(cgi, io)

receptor = Receptor(None, None)
receptor.execute(cgi, io)

echo = Echo(None, None)
echo.execute(cgi, io)
import os
from typing import Optional

class Command:
    def __init__(self, log: Optional[object] = None, lock: Optional[object] = None):
        self.log = log
        self.lock = lock

    def execute(self, CGI: object, IO: object) -> None:
        pass  # Implement execute method

class GetMol(Command):
    def __init__(self, log: Optional[object], lock: Optional[object]):
        super().__init__(log, lock)

    def execute(self, CGI: object, IO: object) -> None:
        IO.write("<html><body>\n")
        for f in CGI.getFiles():
            IO.write(f.getData())
        IO.write("</body></html>\n")

class Echo(Command):
    def __init__(self, log: Optional[object], lock: Optional[object]):
        super().__init__(log, lock)

    def execute(self, CGI: object, IO: object) -> None:
        IO.write("<html><body>")
        IO.write("<textarea>")
        for f in CGI.getFiles():
            IO.write(f.getData())
        IO.write("</textarea>")
        IO.write("</body></html>")

class SaveData(Command):
    def __init__(self, log: Optional[object], lock: Optional[object]):
        super().__init__(log, lock)

    def execute(self, CGI: object, IO: object) -> None:
        content_type = "text/plain"
        if CGI.tagExists("type"):
            content_type = CGI.getString("type")
        filename = "result.txt"
        if CGI.tagExists("fname"):
            filename = CGI.getString("fname")

        IO.write(f"Content-Type: {content_type}\n")
        IO.write(f"Content-Disposition: attachment; filename={filename}\n")
        IO.write("\n")
        IO.write(CGI.getString("data"))

class GetStatus(Command):
    def __init__(self, log: Optional[object], lock: Optional[object], qs: object):
        super().__init__(log, lock)
        self.queries = qs

    def execute(self, CGI: object, IO: object) -> None:
        active_queries, total_queries = self.queries.status()
        IO.write(f"Active Queries: {active_queries}, Total Queries: {total_queries}")

    def is_active(self) -> bool:
        return True  # Implement logic to check if the command is active

class SminaCommand(Command):
    def __init__(self, log: Optional[object], lock: Optional[object], server: str, port: int):
        super().__init__(log, lock)
        self.server = server
        self.port = port

class StartSmina(SminaCommand):
    def __init__(self, log: Optional[object], lock: Optional[object], qs: object, logdirpath: str, server: str, port: int):
        super().__init__(log, lock, server, port)
        self.logdirpath = logdirpath
        self.queries = qs

    def execute(self, CGI: object, IO: object) -> None:
        if not self.server:
            sendError(IO, CGI, "No minimization server configured")
            return

        query = getQuery(CGI, IO)
        if query:
            nR = query.numResults()
            with logmutex:
                max_results = cgiGetInt(CGI, "num")
                t = os.times()
                print(f"startmin {t} {CGI.getEnvironment().getRemoteHost()} {nR} {max_results} {cgiGetInt(CGI, 'qid')}")
                log.flush()

            receptor_id = cgiGetString(CGI, "receptorid")
            if not receptor_id:
                sendError(IO, CGI, "Invalid receptor id.")
                return

            receptor_path = os.path.join(self.logdirpath, receptor_id)
            if os.path.exists(receptor_path):
                with open(receptor_path, 'r') as rec:
                    receptor = rec.read()
            else:
                sendError(IO, CGI, "Missing receptor.")
                return

            filename = cgiGetString(CGI, "recname")
            if not filename:
                sendError(IO, CGI, "Missing receptor filename.")
                return

            rformat = OBConversion.FormatFromExt(filename)
            conv = OBConversion()
            conv.SetInFormat(rformat)
            conv.SetOutFormat("PDBQT")
import os
from io import StringIO
from urllib.parse import urlparse

class SminaCommand:
    def __init__(self, log_file, lock_manager, query_manager, server, port):
        self.log_file = log_file
        self.lock_manager = lock_manager
        self.query_manager = query_manager
        self.server = server
        self.port = port

    def get_query(self, CGI, IO):
        # Implement logic to get the query from CGI and handle errors
        pass

    def send_error(self, IO, CGI, message):
        # Implement logic to send an error response
        pass

class SubmitSmina: SminaCommand:
    def execute(self, CGI, IO):
        receptor = None
        with open(r_path, 'r') as rec:
            receptor = rec.read()
        if not receptor:
            self.send_error(IO, CGI, "Missing receptor.")
            return

        filename = CGI.get("recname")
        if not filename:
            self.send_error(IO, CGI, "Missing receptor filename.")
            return

        rformat = OBConversion.FormatFromExt(filename)
        conv = OBConversion()
        conv.SetInFormat(rformat)
        conv.SetOutFormat("PDBQT")

        # Continue with the rest of the logic...

class GetSminaMol: SminaCommand:
    def execute(self, CGI, IO):
        query = self.get_query(CGI, IO)
        if query:
            if "molid" not in CGI:
                self.send_error(IO, CGI, "Missing id.")
                return
            mid = int(CGI["molid"])
            IO << HTTPPlainHeader()
            sminaid = query.getSminaID()

            with boost.asio.ip.tcp.iostream(self.server, self.port) as strm:
                if not strm:
                    IO << "{\"status\" : 0, \"msg\" : \"ERROR contacting minimization server.\"}\n"
                    return
                strm << "getmols\n" << sminaid << "\n"
                # Continue with the rest of the logic...

class SaveSmina: SminaCommand:
    def execute(self, CGI, IO):
        query = self.get_query(CGI, IO)
        if query:
            nR = query.numResults()
            lock = self.lock_manager.acquire()
            max_results = int(CGI["num"])
            t = datetime.datetime.now()
            print(f"save {t} {CGI['REMOTE_HOST']} {nR} {max_results} {int(CGI['qid'])}", file=self.log_file)
            self.log_file.flush()
            lock.release()

            IO << "Content-Type: text/sdf\n"
            IO << "Content-Disposition: attachment; filename=minimized_results.sdf.gz\n"
            IO << "\n"

            with boost.asio.ip.tcp.iostream(self.server, self.port) as strm:
                if not strm:
                    IO << "ERROR contacting minimization server.\n"
                    return
                strm << "getmols\n" << query.getSminaID() << "\n"
                param = SminaParameters(CGI)
                param.write(strm)
                # Continue with the rest of the logic...

class SminaParameters:
    def __init__(self, CGI):
        self.start = int(CGI.get("start", 0))
        self.num = int(CGI.get("length", 10))
        sortcol = int(CGI.get("order[0][column]", 2))
        if sortcol == 3:
            self.sortType = 0
        elif sortcol == 4:
            self.sortType = 1
        else:
            self.sortType = 2

        dir = CGI.get("order[0][dir]", "asc")
        self.reverseSort = dir in ["desc", "dsc"]

        if "maxscore" in CGI:
            self.maxScore = float(CGI["maxscore"])
        else:
            self.maxScore = float('inf')

        if "maxrmsd" in CGI:
            self.maxRMSD = float(CGI["maxrmsd"])
        else:
            self.maxRMSD = float('inf')

        if "unique" in CGI:
            self.unique = int(CGI["unique"])
        else:
            self.unique = 0

    def write(self, out):
        out.write(f"{self.maxRMSD} {self.maxScore} {self.start} {self.num} {self.sortType} {int(self.reverseSort)} {self.unique}\n")
class SminaParameters:
    def __init__(self, CGI):
        self.maxScore = float(CGI.get("maxscore", 'inf'))
        self.maxRMSD = float(CGI.get("maxrmsd", 'inf'))
        self.unique = int(CGI.get("unique", 0))

    def write(self, out):
        out.write(f"{self.maxRMSD} {self.maxScore} {self.start} {self.num} {self.sortType} {int(self.reverseSort)} {self.unique}\n")

class GetSminaData(SminaCommand):
    def __init__(self, l, lm, qs, s, p):
        super().__init__(l, lm, qs, s, p)

    def execute(self, CGI, IO):
        query = self.getQuery(CGI, IO)
        if query:
            IO.write(HTTPPlainHeader())
            sminaid = query.getSminaID()
            param = SminaParameters(CGI)
            try:
                with socket.create_connection((server, port)) as sock:
                    with sock.makefile('rw') as strm:
                        if not strm:
                            IO.write("{\"status\" : 0, \"error\" : \"Could not connect to minimization server.\"}")
                            return

                        drawcode = cgiGetInt(CGI, "draw")

                        strm.write("getjsonscores\n")
                        strm.write(f"{sminaid} {drawcode}\n")
                        param.write(strm)

                        copy_stream(IO, strm)
            except Exception as e:
                IO.write("{\"status\" : 0, \"error\" : \"Could not connect to minimization server.\"}")

    def isFrequent(self):
        return True