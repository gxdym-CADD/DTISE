"""
Pharmit
Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
All rights reserved.

Pharmit is licensed under both the BSD 3-clause license and the GNU
Public License version 2. Any use of the code that retains its reliance
on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

Use of the Pharmit code independently of OpenBabel (or any other
GPL2 licensed software) may choose between the BSD or GPL licenses.

See the LICENSE file provided with the distribution for more information.
"""

"""
main.py

Created on: Jul 30, 2010
Author: dkoes

Pharmacophore tools for recognition and search.
Really these would probably more suited as their own executables,
but I'm too lazy to move away from Eclipe's default make process which
requires a single target.
"""

import sys
import os
import signal
import subprocess
from argparse import ArgumentParser, Namespace
from typing import List

# Placeholder for CommandLine2::CommandLine and other dependencies
class CommandLine:
    def __init__(self):
        self.Quiet = False
        self.ShowQuery = False
        self.Print = True
        self.Cmd = ""
        self.Database: List[str] = []
        self.inputFiles: List[str] = []
        self.outputFiles: List[str] = []

        self.pharmaSpec = ""
        self.NThreads = 1
        self.MaxRMSD = float('inf')
        self.MinWeight = 0
        self.MaxWeight = sys.maxsize
        self.MinNRot = 0
        self.MaxNRot = sys.maxsize

        self.ReduceConfs = 0
        self.MaxOrient = sys.maxsize
        self.MaxHits = sys.maxsize
        self.Port = 17000
        self.LogDir = "."
        self.ExtraInfo = False
        self.SortRMSD = False
        self.FilePartition = False
        self.Single = ""
        self.SingleSplit = ""

        self.SpecificTimestamp = ""

        self.MinServer = ""
        self.MinPort = 0

        self.Receptor = ""

    def parse_args(self, args):
        # Placeholder for argument parsing logic
        pass

# Placeholder functions and classes for dependencies
class PharmerQuery:
    pass

class PharmerDB:
    pass

class Timer:
    pass

class MolFilter:
    pass

class PharmerServer:
    pass

class ShapeConstraints:
    pass

class ReadMCMol:
    pass

class DBLoader:
    pass

class MinimizationSupport:
    pass

def main():
    cl = CommandLine()
    parser = ArgumentParser(description="Pharmacophore tools for recognition and search.")
    parser.add_argument("-q", "--quiet", action="store_true", help="quiet; suppress informational messages")
    parser.add_argument("--show-query", action="store_true", help="print query points")
    parser.add_argument("--print", action="store_true", help="print results")
    parser.add_argument("cmd", help="command [pharma, dbcreate, dbcreateserverdir, dbsearch, server]")
    parser.add_argument("-dbdir", "--database", nargs='+', help="database directory(s)")
    parser.add_argument("-in", "--input-files", nargs='+', help="input file(s)")
    parser.add_argument("-out", "--output-files", nargs='+', help="output file(s)")

    parser.add_argument("--pharmaspec", help="pharmacophore specification")
    parser.add_argument("--nthreads", type=int, default=1, help="number of threads")
    parser.add_argument("--max-rmsd", type=float, default=float('inf'), help="maximum RMSD value")
    parser.add_argument("--min-weight", type=int, default=0, help="minimum weight value")
    parser.add_argument("--max-weight", type=int, default=sys.maxsize, help="maximum weight value")
    parser.add_argument("--min-nrot", type=int, default=0, help="minimum number of rotations")
    parser.add_argument("--max-nrot", type=int, default=sys.maxsize, help="maximum number of rotations")

    parser.add_argument("--reduce-confs", type=int, default=0, help="reduce conformations")
    parser.add_argument("--max-orient", type=int, default=sys.maxsize, help="maximum orientation value")
    parser.add_argument("--max-hits", type=int, default=sys.maxsize, help="maximum number of hits")
    parser.add_argument("-p", "--port", type=int, default=17000, help="server port")
    parser.add_argument("--logdir", default=".", help="log directory for server")
    parser.add_argument("--extra-info", action="store_true", help="Output additional molecular properties. Slower.")
    parser.add_argument("--sort-rmsd", action="store_true", help="Sort results by RMSD.")
    parser.add_argument("--file-partition", action="store_true", help="Partion database slices based on files")
    parser.add_argument("-s", "--singledir", help="Specify a single directory to recreate on a dbcreateserverdir command")
    parser.add_argument("-ss", "--singlesplit", help="Specify a single directory split to recreate on a dbcreateserverdir command")

    parser.add_argument("--timestamp", help="Specify timestamp to use for server dirs (for use with single)")

    parser.add_argument("--min-server", help="minimization server address")
    parser.add_argument("--min-port", type=int, default=0, help="port for minimization server")

    parser.add_argument("-r", "--receptor", help="Receptor file for interaction pharmacophroes")

    args = parser.parse_args()
    cl.parse_args(args)

    # Placeholder logic for command execution
    if cl.Cmd == "pharma":
        pass
    elif cl.Cmd == "dbcreate":
        pass
    elif cl.Cmd == "dbcreateserverdir":
        pass
    elif cl.Cmd == "dbsearch":
        pass
    elif cl.Cmd == "server":
        pass

if __name__ == "__main__":
    main()
import argparse
import json
from typing import Callable, List

class PharmaPoint:
    def __init__(self, pharma, x, y, z):
        self.pharma = pharma
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"PharmaPoint(pharma={self.pharma}, x={self.x}, y={self.y}, z={self.z})"

class ShapeConstraints:
    def addToJSON(self, root):
        pass

def convertPharmaJson(root, points):
    pass

class OBConversion:
    def SetOutFormat(self, format: str):
        pass

    def Write(self, mol, out):
        pass

class OBMol:
    def NewAtom(self):
        return OBAtom()

class OBAtom:
    def SetAtomicNum(self, atomic_num_label):
        pass

    def SetVector(self, x, y, z):
        pass

class JSonQueryParser:
    def parse(self, pharmas, in_file, points: List[PharmaPoint], excluder: ShapeConstraints):
        pass

class PH4Parser:
    def parse(self, pharmas, in_file, points: List[PharmaPoint], excluder: ShapeConstraints):
        pass

class PMLParser:
    def parse(self, pharmas, in_file, points: List[PharmaPoint], excluder: ShapeConstraints):
        pass

class TextQueryParser:
    def parse(self, pharmas, in_file, points: List[PharmaPoint], excluder: ShapeConstraints):
        pass

pharmaOutputFn = Callable[[str, List[PharmaPoint], ShapeConstraints], None]

def pharmaNoOutput(out: str, points: List[PharmaPoint], excluder: ShapeConstraints):
    pass

def pharmaTxtOutput(out: str, points: List[PharmaPoint], excluder: ShapeConstraints):
    for point in points:
        print(point, file=out)

def pharmaJSONOutput(out: str, points: List[PharmaPoint], excluder: ShapeConstraints):
    root = json.loads("{}")
    convertPharmaJson(root, points)
    excluder.addToJSON(root)
    json.dump(root, out, indent=4)

def pharmaSDFOutput(out: str, points: List[PharmaPoint], excluder: ShapeConstraints):
    conv = OBConversion()
    conv.SetOutFormat("SDF")
    mol = OBMol()

    for point in points:
        atom = mol.NewAtom()
        atom.SetAtomicNum(point.pharma)
        atom.SetVector(point.x, point.y, point.z)

    conv.Write(mol, out)

def handle_pharma_file(fname: str, pharmas, output_files: List[str]):
    import os
    ext = os.path.splitext(fname)[1]
    if ext in ['.json', '.ph4', '.query', '.txt', '.pml']:
        with open(fname, 'r') as in_file:
            points = []
            excluder = ShapeConstraints()
            parser = None

            if ext in ['.json', '.query']:
                parser = JSonQueryParser()
            elif ext == '.ph4':
                parser = PH4Parser()
            elif ext == '.pml':
                parser = PMLParser()
            else:
                parser = TextQueryParser()

            parser.parse(pharmas, in_file, points, excluder)

            if len(output_files) > 0:
                output_ext = os.path.splitext(output_files[0])[1]
                outfn = None
                if output_ext == '.txt' or output_ext == '':
                    outfn = pharmaTxtOutput
                elif output_ext == '.json':
                    outfn = pharmaJSONOutput
                elif output_ext == '.sdf':
                    outfn = pharmaSDFOutput
                else:
                    print("Unsupported output format")
                    return

                with open(output_files[0], 'w') as out_file:
                    outfn(out_file, points, excluder)
    else:
        # pharma recognition
        conv = OBConversion()
        format = conv.FormatFromExt(fname)
        if format is None:
            print(f"Invalid input file format {fname}")
            return

def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', type=str, required=True, help='Input file')
    parser.add_argument('--output', type=str, nargs='+', help='Output files')
    args = parser.parse_args()

    pharmas = []  # Assuming this is populated elsewhere
    handle_pharma_file(args.input, pharmas, args.output)

if __name__ == "__main__":
    main()
import argparse
import sys
from typing import List, Tuple

def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input', type=str, required=True, help='Input file')
    parser.add_argument('--output', type=str, nargs='+', help='Output files')
    args = parser.parse_args()

    pharmas = []  # Assuming this is populated elsewhere
    handle_pharma_file(args.input, pharmas, args.output)

def handle_pharma_file(fname: str, pharmas: List, output_files: List[str]):
    if not fname:
        print(f"Invalid input file format {fname}")
        return

    conv = OBConversion()
    format = conv.FormatFromExt(fname)
    if format is None:
        sys.stderr.write(f"Invalid input file format {fname}\n")
        sys.exit(-1)

    conv.SetInFormat(format)
    mol = OBMol()
    points: List[PharmaPoint] = []

    receptor = OBMol()
    if Receptor.size() > 0:
        rconv = OBConversion()
        rformat = rconv.FormatFromExt(Receptor)
        if format:
            rconv.SetInFormat(rformat)
            with open(Receptor, 'r') as rin:
                rconv.Read(receptor, rin)

    aromatics = OBAromaticTyper()
    atyper = OBAtomTyper()
    with open(fname, 'r') as in_file:
        while conv.Read(mol, in_file):
            mol.AddHydrogens()

            mol.FindRingAtomsAndBonds()
            PerceiveStereo(mol)
            mol.PerceiveBondOrders()
            aromatics.AssignAromaticFlags(mol)
            mol.FindSSSR()
            atyper.AssignTypes(mol)
            atyper.AssignHyb(mol)

            if receptor.NumAtoms() > 0:
                screenedout: List[PharmaPoint] = []
                getInteractionPoints(pharmas, receptor, mol, points, screenedout)
            elif Receptor.size() > 0:
                sys.stderr.write(f"No atoms in {Receptor}\n")
                sys.exit(-1)
            else:
                getPharmaPoints(pharmas, mol, points)

            dummy = ShapeConstraints()
            if not Quiet:
                pharmaTxtOutput(sys.stdout, points, dummy)
            outfn(output_files, points, dummy)

def sigv_handler(sig: int):
    import traceback
    print(f"Error: signal {sig}:", file=sys.stderr)
    traceback.print_stack(file=sys.stderr)
    sys.exit(1)

def handle_fixsmina_cmd():
    from pathlib import Path

    for i in range(len(inputFiles)):
        fname = inputFiles[i]
        if not fname:
            continue

        path = Path(fname)
        if not path.exists():
            print(f"File {fname} does not exist", file=sys.stderr)
            continue

        with open(path, 'r') as f:
            lines = f.readlines()

        # Process the lines here
        processed_lines = [line.strip() for line in lines]

        with open(path, 'w') as f:
            f.writelines(processed_lines)

if __name__ == "__main__":
    main()
import os
import sys
from pathlib import Path

def main():
    input_files = ["file1.txt", "file2.txt"]  # Example input files
    for i, fname in enumerate(input_files):
        if not fname:
            continue

        path = Path(fname)
        if not path.exists():
            print(f"File {fname} does not exist", file=sys.stderr)
            continue

        with open(path, 'r') as f:
            lines = f.readlines()

        # Process the lines here
        processed_lines = [line.strip() for line in lines]

        with open(path, 'w') as f:
            f.writelines(processed_lines)

if __name__ == "__main__":
    main()
import os
import sys
from pathlib import Path

def handle_phogrify_cmd(pharmas):
    if len(output_files) > 0 and len(output_files) != len(input_files):
        sys.stderr.write("Number of outputs must equal number of inputs.\n")
        sys.exit(-1)

    for i, fname in enumerate(input_files):
        with open(fname, 'r') as f:
            lines = f.readlines()

        # Process the lines here
        processed_lines = [line.strip() for line in lines]

        with open(output_files[i] if output_files else fname, 'w') as f:
            f.writelines(processed_lines)

if __name__ == "__main__":
    main()
import os
import sys
from pathlib import Path

def handle_dbcreate_cmd(pharmas):
    if not database_directory:
        sys.stderr.write("Need to specify location of database directory to be created.\n")
        sys.exit(-1)

    # Create directories
    for db_dir in database_directory:
        os.makedirs(db_dir, exist_ok=True)

    # Check and setup input
    num_bytes = 0
    for fname in input_files:
        if not Path(fname).exists():
            sys.stderr.write(f"Invalid input file: {fname}\n")
            sys.exit(-1)
        # Assuming a function to get format from extension
        format = get_format_from_extension(fname)
        if not format:
            sys.stderr.write(f"Invalid input format: {fname}\n")
            sys.exit(-1)

        num_bytes += Path(fname).stat().st_size

    # Create databases
    for db_dir in database_directory:
        if len(database_directory) == 1 or os.fork() == 0:
            db = PharmerDatabaseCreator(pharmas, db_dir)
            unique_id = 1
            # Now read files
            read_bytes = 0
            for fname in input_files:
                if file_partition and i % len(database_directory) != d:
                    continue
                with open(fname, 'r') as f:
                    lines = f.readlines()
                    # Process the lines here
                    processed_lines = [line.strip() for line in lines]
                    db.add_molecule(processed_lines)
            sys.exit(0)

if __name__ == "__main__":
    main()
import os
import sys
import json
from typing import List, Tuple

class LigandInfo:
    def __init__(self):
        self.file = ""
        self.id: int = 0
        self.name: str = ""

def handle_dbcreateserverdir_cmd(pharmas):
    from signal import SIGUSR1, signal
    import boost.filesystem as fs

    def signalhandler(sig):
        pass

    signal(SIGUSR1, signalhandler)

    with open(Prefixes, 'r') as prefixes_file:
        if not Prefixes or not prefixes_file.read():
            print("Problem with prefixes.")
            sys.exit(-1)

    with open(DBInfo, 'r') as dbinfo_file:
        if not DBInfo or not dbinfo_file.read():
            print("Problem with database info.")
            sys.exit(-1)

    if not fs.exists(Ligands):
        print("Need ligand file")
        sys.exit(-1)

    import json
    root = json.load(dbinfo_file)
    if "subdir" not in root:
        print("Database info needs subdir field.")
        sys.exit(-1)

    liginfos: List[LigandInfo] = []
    with open(Ligands, 'r') as ligs_file:
        for line in ligs_file:
            parts = line.split()
            if len(parts) < 3:
                print("Error in ligand file on line:\n", line)
                sys.exit(-1)

            info = LigandInfo()
            info.file = parts[0]
            info.id = int(parts[1])
            info.name = ' '.join(parts[2:])
            liginfos.append(info)

    key = root["subdir"]
    if SpecificTimestamp:
        key += f"-{SpecificTimestamp}"
    else:
        key += f"-{int(time.time())}"

    subset = root["subdir"]

    if "maxconfs" in root and isinstance(root["maxconfs"], int):
        if ReduceConfs == 0:
            ReduceConfs = root["maxconfs"]
        else:
            print("Warning: -reduceconfs overriding dbinfo")

    splits: List[str] = []
    if "splitdirs" in root and isinstance(root["splitdirs"], list):
        splits = [sdir for sdir in root["splitdirs"]]

    directories: List[fs.path] = []
    unflatdirectories: List[List[fs.path]] = []
    topdirectories: List[fs.path] = []
    symlinks: List[fs.path] = []

    with open(Prefixes, 'r') as prefixes_file:
        for fname in prefixes_file:
            fname = fname.strip()
            if fname and not fname.startswith('#'):
                dbpath = fs.path(fname) / key
                topdirectories.append(dbpath)

# The rest of the code would continue similarly, adapting C++ constructs to Python.
import os
from typing import List, Optional
from pathlib import Path
import subprocess

directories: List[Path] = []
unflatdirectories: List[List[Path]] = []
topdirectories: List[Path] = []
symlinks: List[Path] = []

with open(Prefixes, 'r') as prefixes_file:
    for fname in prefixes_file:
        fname = fname.strip()
        if fname and not fname.startswith('#'):
            dbpath = Path(fname) / key
            topdirectories.append(dbpath)

# The rest of the code would continue similarly, adapting C++ constructs to Python.

for fname in topdirectories:
    if not os.path.exists(fname):
        print(f"Prefix {fname} does not exist")
        continue

    dbpath = Path(fname)
    dbpath /= key

    topdirectories.append(dbpath)
    unflatdirectories.append([])  # needs splits to be dispersed
    if len(splits) > 0:  # create a bunch of subdirs
        for split in splits:
            splitdb = dbpath / split
            if SingleSplit and split == SingleSplit:
                singlesplits.add(splitdb)

            os.makedirs(splitdb, exist_ok=True)
            unflatdirectories[-1].append(splitdb)
    else:
        os.makedirs(dbpath, exist_ok=True)
        unflatdirectories[-1].append(dbpath)

    # single link for the whole thing
    link = Path(fname) / subset
    symlinks.append(link)

# flatten directories
while True:
    i = 0
    n = len(unflatdirectories)
    for _ in range(n):
        if not unflatdirectories[i]:
            break
        directories.append(unflatdirectories[i].pop())
        i += 1
    if i != n:
        break

# portion memory between processes
memsz = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
memsz //= len(directories)
memsz //= 2  # only take half of available memory

maxt = len(topdirectories)  # single thread per i/o device
numrunning = 0
# multi-thread (fork actually, due to openbabel) across all prefixes
# create databases
# openbabel can't handled multithreaded reading, so we actually have to fork off a process
# for each database
for d in range(len(directories)):
    if d == len(directories) - 1 or subprocess.Popen(['python', '-c', 'pass']).poll() is not None:
        numrunning += 1
        if numrunning >= maxt:  # using all threads
            subprocess.wait()
            numrunning -= 1

# wait for all child processes to complete
while True:
    pid, status = os.waitpid(-1, os.WNOHANG)
    if pid == 0:
        break
    if not os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
        os.abort()

# all done, create symlinks to non-timestamped directories
assert len(symlinks) == len(topdirectories)
for d in range(len(topdirectories)):
    if os.path.exists(symlinks[d]):
        # remove preexisting symlink
        if os.path.islink(symlinks[d]):
            os.remove(symlinks[d])
        else:
            print(f"Trying to replace a non-symlink: {symlinks[d]}")
import os
import sys
import json
from pathlib import Path
from shutil import rmtree, symlink_to
from concurrent.futures import ThreadPoolExecutor

# Assuming the existence of necessary classes and functions like PharmerQuery, StripedSearchers, etc.

def handle_pharma_cmd(pharmas):
    # Implementation for handling pharma command
    pass

def handle_phogrify_cmd(pharmas):
    # Implementation for handling phogrify command
    pass

def sigv_handler(signum, frame):
    # Implementation for signal handler
    pass

def loadDatabases(dbpaths, databases):
    # Implementation to load databases
    pass

class Timer:
    def __init__(self):
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time

class QueryParameters:
    def __init__(self):
        self.maxRMSD = None
        self.minWeight = None
        self.maxWeight = None
        self.minRot = None
        self.maxRot = None
        self.reduceConfs = None
        self.orientationsPerConf = None
        self.maxHits = None
        self.sort = None

class DataParameters:
    def __init__(self):
        self.extraInfo = None
        self.sort = None

class PharmerQuery:
    @staticmethod
    def validFormat(extension):
        # Implementation to check valid format
        pass

    def __init__(self, stripes, qfile, extension, params, num_threads):
        # Initialization for PharmerQuery
        pass

    def isValid(self, err):
        # Check if query is valid
        pass

    def print(self, cout):
        # Print query details
        pass

    def execute(self):
        # Execute query
        pass

    def outputData(self, dparams, out):
        # Output data to stream
        pass

    def outputMols(self, out):
        # Output molecules to stream
        pass

    def numResults(self):
        # Return number of results
        pass

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("Cmd", choices=["pharma", "phogrify"])
    parser.add_argument("--Database", nargs="+")
    parser.add_argument("--pharmaSpec")
    args = parser.parse_args()

    Cmd = args.Cmd
    Database = args.Database
    pharmaSpec = args.pharmaSpec

    pharmas = defaultPharmaVec
    if pharmaSpec:
        with open(pharmaSpec, 'r') as pharmin:
            if not pharmas.read(pharmin):
                sys.stderr.write("Invalid pharmacophore specification file.\n")
                sys.exit(1)

    if Cmd == "pharma":
        handle_pharma_cmd(pharmas)
    elif Cmd == "phogrify":
        handle_phogrify_cmd(pharmas)

if __name__ == "__main__":
    main()
import sys
from pathlib import Path

def main(args):
    Cmd = args.Cmd
    Database = args.Database
    pharmaSpec = args.pharmaSpec

    pharmas = defaultPharmaVec
    if pharmaSpec:
        with open(pharmaSpec, 'r') as pharmin:
            if not pharmas.read(pharmin):
                sys.stderr.write("Invalid pharmacophore specification file.\n")
                sys.exit(1)

    if Cmd == "pharma":
        handle_pharma_cmd(pharmas)
    elif Cmd == "phogrify":
        handle_phogrify_cmd(pharmas)
    elif Cmd == "showpharma":
        pharmas.write(sys.stdout)
    elif Cmd == "dbcreate":
        handle_dbcreate_cmd(pharmas)
    elif Cmd == "dbcreateserverdir":
        handle_dbcreateserverdir_cmd(pharmas)
    elif Cmd == "dbsearch":
        handle_dbsearch_cmd()
    elif Cmd == "fixsmina":
        handle_fixsmina_cmd()
    elif Cmd == "server":
        prefixpaths = []
        databases = {}

        # total hack time - fcgi uses select which can't
        # deal with file descriptors higher than 1024, so let's reserve some
        MAXRESERVEDFD = SERVERTHREADS * 2
        reservedFD = [open("/dev/null", "r").fileno() for _ in range(MAXRESERVEDFD)]

        # loadDatabases will open a whole bunch of files
        if args.Prefixes and Database:
            sys.stderr.write("Cannot specify both dbdir and prefixes\n")
            sys.exit(-1)
        elif Database:
            # only one subset
            dbpaths = [Path(db) for db in Database]
            loadDatabases(dbpaths, databases[""])
        else:
            # use prefixes
            with open(args.Prefixes, 'r') as prefixes:
                line = prefixes.readline().strip()
                while line:
                    if Path(line).exists():
                        prefixpaths.append(Path(line))
                    else:
                        sys.stderr.write(f"{line} does not exist\n")
                    line = prefixes.readline().strip()

        if not prefixpaths:
            sys.stderr.write("No valid prefixes\n")
            sys.exit(-1)

        loadFromPrefixes(prefixpaths, databases)

        # now free reserved fds
        for fd in reservedFD:
            os.close(fd)

        pharmer_server(args.Port, prefixpaths, databases, args.LogDir, args.MinServer, args.MinPort)
    else:
        cl.PrintHelpMessage()
        if not Cmd:
            sys.stderr.write("Command [pharma, dbcreate, dbsearch] required.\n")
        else:
            sys.stderr.write(f"{Cmd} not a valid command.\n")
        sys.exit(-1)

if __name__ == "__main__":
    main(args)