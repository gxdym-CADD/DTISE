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
cors.py

Classes for maintaining correspondences between point sets.
A correspondence just associates one set of indices with another;
in this case the indices of the query with the indices of the mol.

Created on: Aug 8, 2010
Author: dkoes
"""

import struct
import json
from typing import List

matchType = int

class CorrespondenceInline:
    def __init__(self, n: int):
        self.size = n
        self.match = [-1] * n

    def matchIndex(self, i: int) -> int:
        if self.match[i] == 255:
            return -1
        return self.match[i]

    def print(self, out):
        for i in range(self.size):
            out.write(f"{self.match[i]}")
            if i < self.size - 1:
                out.write(" ")

    def setIndex(self, i: int, s: int):
        self.match[i] = s

    def clear(self):
        self.match = [-1] * self.size

    def writeJSON(self, out):
        out.write("[")
        for i in range(self.size):
            out.write(f"{self.match[i]}")
            if i < self.size - 1:
                out.write(",")
        out.write("]")

class CorrespondenceResult:
    def __init__(self, numPoints: int):
        self.location = 0
        self.rmsd = RMSDResult()  # Assuming RMSDResult is defined elsewhere
        self.val = 0.0
        self.weight = 0.0
        self.molid = 0
        self.dbid = 0
        self.nRBnds = 0
        self.cor = CorrespondenceInline(numPoints)

    def reinitialize(self, tm: TripletMatch, db: int, numdb: int):
        self.location = tm.id * numdb + db
        self.weight = tm.weight
        self.nRBnds = tm.nRBnds
        self.molid = tm.molid * numdb + db
        self.dbid = tm.molid
        self.rmsd.clear()
        self.cor.clear()

class CorAllocator:
    def __init__(self, qsz: int = 0):
        self.qsize = qsz
        self.Csize = struct.calcsize(f"I{qsz}B") if qsz > 0 else 0
        self.CRsize = struct.calcsize(f"QfIfIIH{qsz}B") if qsz > 0 else 0
        self.allocator = BumpAllocator(1024 * 1024)  # Assuming BumpAllocator is defined elsewhere

    def setSize(self, qsz: int):
        self.qsize = qsz
        self.Csize = struct.calcsize(f"I{qsz}B")
        self.CRsize = struct.calcsize(f"QfIfIIH{qsz}B")

    def newCor(self) -> CorrespondenceInline:
        ptr = self.allocator.alloc(self.Csize)
        return CorrespondenceInline(self.qsize)

    def newCorResult(self, c: CorrespondenceResult) -> CorrespondenceResult:
        ptr = self.allocator.alloc(self.CRsize)
        return CorrespondenceResult(self.qsize)

    def newCorResult(self) -> CorrespondenceResult:
        ptr = self.allocator.alloc(self.CRsize)
        return CorrespondenceResult(self.qsize)

    def clear(self):
        self.allocator.clear()

    def numChunks(self) -> int:
        return self.allocator.numChunks()