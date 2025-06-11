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
pharmerdb.py

Created on: Aug 2, 2010
Author: dkoes

Creation and search routines for the specially formatted pharmer database.
"""

from typing import List, Optional
import os
import struct
import openbabel as ob

class PointDataFile:
    def __init__(self, name: str = "", p: int = 0):
        self.name = name
        self.file = None
        self.length = 0
        self.phTrip = p

    def is_valid(self) -> bool:
        return self.file is not None

    def write(self, ptr: bytes, size: int, nmemb: int):
        if nmemb == 0 or size == 0:
            return
        if self.file is None:
            self.file = open(self.name, "wb+")
            assert self.file
            # POSIX_FADV_SEQUENTIAL equivalent in Python can be handled with os.posix_fadvise if available

        self.file.write(ptr * nmemb)
        self.length += size * nmemb

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

class MolDataHeader:
    __slots__ = ["molID", "molWeight", "confidx"]

    def __init__(self, mid: int = 0, mw: float = 0.0, cid: int = 0):
        self.molID = mid
        self.molWeight = mw
        self.confidx = cid

    def pack(self) -> bytes:
        return struct.pack("<IIfH", self.molID, self.molWeight, self.confidx)

class ConfCreator:
    __slots__ = ["header", "molData"]

    def __init__(self, mid: int, mw: float, cid: int, mol: ob.OBMol):
        self.header = MolDataHeader(mid, mw, cid)
        # Assuming molData is a string representation of the molecule
        self.molData = str(mol)

    def byte_size(self) -> int:
        return struct.calcsize("<IIfH") + len(self.molData.encode('utf-8'))

    def write(self, buf: bytearray) -> int:
        header_data = self.header.pack()
        mol_data = self.molData.encode('utf-8')
        buf.extend(header_data)
        buf.extend(mol_data)
        return self.byte_size()

    def is_valid(self) -> bool:
        return len(self.molData) > 0

class MolDataCreator:
    max_index = 0

    def __init__(self, pharmas: List, tindex: object, mol: ob.OBMol, props: object, mid: int):
        self.pharmas = pharmas
        self.tindex = tindex
        self.confs: List[ConfCreator] = []
        self.confOffsets: List[int] = []
        self.pdatas: List[List] = [[] for _ in range(tindex.size())]
        self.mid = mid
        self.buffer: Optional[bytearray] = None
        self.bufferSize = 0
        self.numConfs = 0

        self.process_mol(mol, props, mid)
        self.create_buffer()

    def __del__(self):
        if self.buffer:
            del self.buffer

    def process_mol(self, mol: ob.OBMol, props: object, mid: int):
        # Placeholder for processing molecule logic
        pass

    def create_buffer(self):
        total_size = 0
        for conf in self.confs:
            total_size += conf.byte_size()
        self.bufferSize = total_size
        self.buffer = bytearray(total_size)

        offset = 0
        for i, conf in enumerate(self.confs):
            offset += conf.write(self.buffer[offset:])
            self.confOffsets.append(offset)

    def write(self, molData: object, pointDataFiles: List[PointDataFile]) -> int:
        if self.buffer is None:
            return 0

        # Assuming molData is a file-like object
        molData.write(self.buffer)
        return len(self.buffer)

    @property
    def NumPoints(self) -> int:
        return sum(len(pd) for pd in self.pdatas)

    @property
    def NumConfs(self) -> int:
        return self.numConfs

    @classmethod
    def MaxIndex(cls) -> int:
        return cls.max_index

    @property
    def ConfOffsets(self) -> List[int]:
        return self.confOffsets
from typing import List, Optional
import numpy as np

class PharmerDatabaseCreator:
    def __init__(self):
        self.dbpath = None  # path to database directory
        self.info = None  # small amount of metadata
        self.lookup = None  # human readable pharmacophore classes for my own benefit
        self.molData = None  # flat file of molecular data
        self.binData = None  # binned cnts of lengths
        self.midList = None  # index of mids corresponding to sequential index

        self.sminaIndex = None  # map from mol location to location in sminadata
        self.sminaData = None  # smina formated molecule

        self.pharmInfoData = None  # pharmacphore data for each molecule, indexed into by shape
        self.tmpFiles = [None] * NUMTMPFILES  # for partitioning

        self.propFiles = MolProperties.PropFiles()

        self.pointDataFiles: List[PointDataFile] = []  # just pointdata objects; separate library for every pharma combo; indexed by triplet index
        self.pointDataArrays: Optional[MMappedRegion[ThreePointData]] = None

    @staticmethod
    def MaxIndex() -> int:
        return maxIndex

    @property
    def ConfOffsets(self) -> List[int]:
        return self.confOffsets

    def getConfFeatures(self, c: int) -> List[PharmaPoint]:
        if c >= len(self.mcpoints):
            raise RuntimeError("Invalid conformation index")
        return self.mcpoints[c]

# data for a single conformation, include full mol since this turns out to
# be faster than more compressed layouts
class MolData:
    def __init__(self):
        self.mol = None  # just the conformation
        self.mid = 0  # mol identifier
        self.molWeight = 0.0
        self.confidx = 0  # which conformation

    def read(self, molData: FILE, areader: PMolReader) -> bool:
        pass

    def read(self, molData: FILE, location: int, areader: PMolReader) -> bool:
        pass

    def read(self, molData: bytes, location: int, areader: PMolReader) -> bool:
        pass

    def readDataOnly(self, molData: bytes, location: int):
        pass

    def clear(self):
        pass

class GeoKDPageNode:
    def __init__(self):
        self.box = BoundingBox()  # bounding box of this entire node
        self.splitVal = 0  # value we are splitting on
        self.splitType = SplitType.NoSplit  # how we are splitting, nosplit means we are a leaf
        self.nextPage = 0

class GeoKDPage:
    SPLITS_PER_GEOPAGE = 256
    MAX_POINTDATAS_PER_LEAF = 10
    MIN_POINTDATAS_PER_PAGE = 2 * SPLITS_PER_GEOPAGE
    MAX_UNIQUE_POINTS_PER_LEAF = 2

    def __init__(self):
        self.nodes = [GeoKDPageNode() for _ in range(self.SPLITS_PER_GEOPAGE)]  # index 0 is unused and can be overloaded
        self.nextPages = [0] * self.SPLITS_PER_GEOPAGE

class QueryPoint:
    pass

class Stats:
    NumMols, NumConfs, NumDbPoints, NumUniquePoints, NumInternalPages, LastStat = range(6)

MCPoints = List[List[PharmaPoint]]

NUMTMPFILES = 3
from typing import List, Tuple, Any
import os

POINTDATAS_PER_LEAF = 10
MIN_POINTDATAS_PER_PAGE = 2 * SPLITS_PER_GEOPAGE
MAX_UNIQUE_POINTS_PER_LEAF = 2

class GeoKDPageNode:
    pass

class QueryPoint:
    pass

class Stats:
    NumMols, NumConfs, NumDbPoints, NumUniquePoints, NumInternalPages, LastStat = range(6)

MCPoints = List[List[Any]]

NUMTMPFILES = 3

class PharmerDatabaseCreator:
    def __init__(self, ps: Any, dbp: str, dbi: Any):
        self.dbpath = dbp
        self.info = None
        self.molData = None
        self.midList = None
        self.sminaIndex = None
        self.sminaData = None
        self.pharmInfoData = None
        self.pointDataArrays = None
        self.pharmas = ps
        self.tindex = TripleIndexer(ps.size())
        self.molDataWorkQ = MTQueue(vector[MolDataCreator*], 32)
        self.mids = []
        self.dbinfo = dbi

        self.stats = [0] * Stats.LastStat

        zero = [[[[0 for _ in range(LENGTH_BINS)] for _ in range(LENGTH_BINS)] for _ in range(LENGTH_BINS)]
        self.binnedCnts = [zero.copy() for _ in range(self.tindex.size())]

        self.initializeDatabases()

        self.leveler.initialize(&self.topdown, &self.packer)
        self.shapedb.initialize(os.path.join(dbp, "shape"), PHARMIT_DIMENSION, PHARMIT_RESOLUTION, &self.leveler)

        memsz = os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGESIZE')
        self.pdatasFitInMemory = 2 * memsz // sizeof(ThreePointData) // 3

    def __del__(self):
        if self.info:
            self.info.close()
        if self.molData:
            self.molData.close()
        if self.midList:
            self.midList.close()

        if self.sminaData:
            self.sminaData.close()
        if self.sminaIndex:
            self.sminaIndex.close()
        if self.pharmInfoData:
            self.pharmInfoData.close()

        for file in self.pointDataFiles:
            file.close()
        for file in self.geoDataFiles:
            if file:
                file.close()

        if self.pointDataArrays is not None:
            del self.pointDataArrays

        for file in self.propFiles:
            if file:
                file.close()

        for i in range(NUMTMPFILES):
            if self.tmpFiles[i]:
                self.tmpFiles[i].close()

    def setInMemorySize(self, maxmem: int):
        self.pdatasFitInMemory = maxmem // sizeof(ThreePointData)

    def addMolToDatabase(self, mol: Any, uniqueid: int, name: str):
        pass

    def createSpatialIndex(self):
        pass

    def writeStats(self):
        pass

    def numMolecules(self) -> int:
        return self.stats[Stats.NumMols]

    def numConformations(self) -> int:
        return self.stats[Stats.NumConfs]

    def getJSON(self) -> Any:
        return self.dbinfo
import json
from typing import Any, List, Tuple

class ThreePointData:
    pass  # Placeholder for ThreePointData class

class GeoKDPage:
    pass  # Placeholder for GeoKDPage class

class QueryTriplet:
    pass  # Placeholder for QueryTriplet class

class TripletMatches:
    pass  # Placeholder for TripletMatches class

class MolProperties:
    class MolPropertyReader:
        def get(self, kind: Any, mid: int) -> float:
            pass  # Placeholder for get method

class ShapeConstraints:
    pass  # Placeholder for ShapeConstraints class

class ShapeResults:
    pass  # Placeholder for ShapeResults class

class PMolReader:
    pass  # Placeholder for PMolReader class

class MolData:
    def read(self, data: Any, location: int, reader: PMolReader) -> bool:
        pass  # Placeholder for read method

    def readDataOnly(self, data: Any, location: int):
        pass  # Placeholder for readDataOnly method

class MMappedRegion:
    def __init__(self, dtype, *args, **kwargs):
        self.data = []

    def length(self) -> int:
        return len(self.data)

    def begin(self):
        return self.data

class Stats:
    NumMols = 0
    NumConfs = 1
    LastStat = 2

class PharmerDatabaseSearcher:
    StartEnd = Tuple[int, int]

    def __init__(self, dbp: str):
        self.dbpath = dbp
        self.info = None
        self.valid = False
        self.inactive = False
        self.emptyCnt = 0
        self.processCnt = 0
        self.matchedCnt = 0

        self.goodChunkSize = 100000  # what's life without a little magic (numbers)?
        self.stats = [0] * Stats.LastStat

        self.initializeDatabases()
        self.pharmas.setDefaultSearchRadius(1.0)  # default search radius _really_ shouldn't be property of database

    def __del__(self):
        if self.tripletDataArrays:
            del self.tripletDataArrays
        if self.geoDataArrays:
            del self.geoDataArrays

    def activate(self):
        if self.inactive:
            with self.lock:
                if self.inactive:
                    self.initializeDatabases()
                self.inactive = False

    def deactivate(self):
        pass  # Placeholder for deactivate method

    def isActive(self) -> bool:
        return not self.inactive

    def numMolecules(self) -> int:
        return self.stats[Stats.NumMols]

    def numConformations(self) -> int:
        return self.stats[Stats.NumConfs]

    def getJSON(self) -> Any:
        return self.dbinfo

    def getBaseMID(self, lmid: int) -> int:
        len_midList = len(self.midList.data)
        if len_midList == 0:
            return lmid
        if lmid >= len_midList:
            return self.midList.data[-1]
        return self.midList.data[lmid]

    def getMolProp(self, kind: Any, mid: int) -> float:
        return self.props.get(kind, mid)

    def rankTriplets(self, triplets: List[QueryTriplet], ranking: List[float]) -> int:
        pass  # Placeholder for rankTriplets method

    def generateTripletMatches(self, triplets: List[List[QueryTriplet]], Q: TripletMatches, stopEarly: bool):
        pass  # Placeholder for generateTripletMatches method

    def generateShapeMatches(self, constraints: ShapeConstraints, results: ShapeResults):
        pass  # Placeholder for generateShapeMatches method

    def getMolData(self, location: int, mdata: MolData, reader: PMolReader) -> bool:
        return mdata.read(self.molData.begin(), location, reader)

    def getSminaData(self, location: int, out):
        pass  # Placeholder for getSminaData method

    def getPharmas(self) -> Any:
        return self.pharmas

    def alignedPharmasMatch(self, phlocation: int, query: List[Any]) -> bool:
        pass  # Placeholder for alignedPharmasMatch method

    def getName(self) -> str:
        return self.dbpath

    def isValid(self) -> bool:
        return self.valid

    def initializeDatabases(self):
        pass  # Placeholder for initializeDatabases method
from typing import List, Any, Optional
import json

class PharmerDatabaseSearcher:
    def __init__(self, dbpath: str):
        self.dbpath = dbpath
        self.valid = False
        self.shapesearch = []
        self.pharmas = []

    def tSminaData(self, location: int, out) -> None:
        pass  # Placeholder for getSminaData method

    def getPharmas(self) -> List[Any]:
        return self.pharmas

    def alignedPharmasMatch(self, phlocation: int, query: List[Any]) -> bool:
        pass  # Placeholder for alignedPharmasMatch method

    def getName(self) -> str:
        return self.dbpath

    def isValid(self) -> bool:
        return self.valid

    def initializeDatabases(self) -> None:
        pass  # Placeholder for initializeDatabases method

    def hasShape(self) -> bool:
        return len(self.shapesearch) > 0

class StripedSearchers:
    def __init__(self):
        self.stripes: List[PharmerDatabaseSearcher] = []
        self.totalConfs: int = 0
        self.totalMols: int = 0
        self.hasShape: bool = True

    def getJSON(self) -> dict:
        assert len(self.stripes) > 0, "StripedSearchers must have at least one stripe"
        ret = self.stripes[0].getJSON()
        totalConfs = sum(stripe.numConformations() for stripe in self.stripes)
        totalMols = sum(stripe.numMolecules() for stripe in self.stripes)
        ret["numConfs"] = totalConfs
        ret["numMols"] = totalMols
        return ret

    def activate(self) -> None:
        for stripe in self.stripes:
            stripe.activate()

    def deactivate(self) -> None:
        for stripe in self.stripes:
            stripe.deactivate()