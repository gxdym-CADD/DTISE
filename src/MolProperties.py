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
MolProperties.py

Created on: Mar 5, 2015
Author: dkoes
"""

import os
from typing import List, Tuple
import openbabel as ob
import numpy as np

class MMappedRegion:
    def __init__(self, dtype, filename):
        self.dtype = dtype
        self.filename = filename
        self.data = np.memmap(filename, dtype=dtype, mode='r+')

    def clear(self):
        self.data.flush()

    def __getitem__(self, index):
        return self.data[index]

class MolProperties:
    uniqueid: int  # user provided namespace for molecules
    num_rings: int
    num_aromatics: int
    hba: int
    hbd: int
    logP: float
    psa: float

    PropIDs = {
        'UniqueID': 0,
        'NRings': 1,
        'NAromatics': 2,
        'LogP': 3,
        'PSA': 4,
        'HBA': 5,
        'HBD': 6,
        'None': 7
    }

    class MolPropertyReader:
        def __init__(self, dbpath):
            self.uniqueid = MMappedRegion(np.uint64, os.path.join(dbpath, "uniqueid.bin"))
            self.num_rings = MMappedRegion(np.uint8, os.path.join(dbpath, "num_rings.bin"))
            self.num_aromatics = MMappedRegion(np.uint8, os.path.join(dbpath, "num_aromatics.bin"))
            self.logP = MMappedRegion(np.float32, os.path.join(dbpath, "logP.bin"))
            self.psa = MMappedRegion(np.float32, os.path.join(dbpath, "psa.bin"))
            self.hba = MMappedRegion(np.uint8, os.path.join(dbpath, "hba.bin"))
            self.hbd = MMappedRegion(np.uint8, os.path.join(dbpath, "hbd.bin"))

        def clear(self):
            self.uniqueid.clear()
            self.num_rings.clear()
            self.num_aromatics.clear()
            self.logP.clear()
            self.psa.clear()
            self.hba.clear()
            self.hbd.clear()

        def get(self, kind: str, pos: int) -> float:
            match kind:
                case 'UniqueID':
                    return self.uniqueid[pos]
                case 'NRings':
                    return self.num_rings[pos]
                case 'NAromatics':
                    return self.num_aromatics[pos]
                case 'LogP':
                    return self.logP[pos]
                case 'PSA':
                    return self.psa[pos]
                case 'HBA':
                    return self.hba[pos]
                case 'HBD':
                    return self.hbd[pos]
                case 'None':
                    return 0
            return 0

    def __init__(self):
        self.uniqueid = 0
        self.num_rings = 0
        self.num_aromatics = 0
        self.hba = 0
        self.hbd = 0
        self.logP = 0.0
        self.psa = 0.0

    def calculate(self, mol: ob.OBMol, id: int):
        # Implementation of the calculate method goes here
        pass

    def setHB(self, pts: List[Tuple[int, int]]):
        # Implementation of the setHB method goes here
        pass

    @staticmethod
    def write(mid: int, files: List[str]):
        # Implementation of the write method goes here
        pass

    @staticmethod
    def createFiles(dbpath: str, files: List[str]):
        # Implementation of the createFiles method goes here
        pass

    @staticmethod
    def initializeReader(dbpath: str, reader: MolPropertyReader):
        # Implementation of the initializeReader method goes here
        pass

    fileNames = [
        "uniqueid.bin",
        "num_rings.bin",
        "num_aromatics.bin",
        "logP.bin",
        "psa.bin",
        "hba.bin",
        "hbd.bin"
    ]