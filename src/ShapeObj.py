# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

from typing import Tuple, List
import numpy as np
from openbabel import pybel

PHARMIT_RESOLUTION = 0.5
PHARMIT_DIMENSION = 32

TPD_MOLDATA_BITS = 40
WEIGHT_BITS = 10
ROTATABLE_BITS = 4

class ShapeObj(pybel.Molecule):
    @staticmethod
    def calcSplitMoments(coords: List[np.ndarray], C: int) -> Tuple[float, float]:
        # Implementation of calcSplitMoments goes here
        pass

    class MolInfo:
        def __init__(self, molPos: int = 0, pharmPos: int = 0, weight: int = 0, nrot: int = 0, extra: int = 0):
            self.molPos = molPos
            self.pharmPos = pharmPos
            self.weight = weight
            self.nrot = nrot
            self.extra = extra

        def __init__(self, m: pybel.Molecule, mPos: int):
            self.molPos = mPos
            self.pharmPos = 0
            self.extra = 0
            self.weight = ThreePointData.reduceWeight(m.mw)
            self.nrot = ThreePointData.reduceRotatable(countRotatableBonds(m))

    def __init__(self, mol: pybel.Molecule, info: MolInfo, dimension: float, resolution: float):
        super().__init__(mol.OBMol)
        self.minfo = info

    def __init__(self, mol: pybel.Molecule, translate: np.ndarray, rotate: np.ndarray, info: MolInfo, dimension: float, resolution: float):
        super().__init__(mol.OBMol)
        self.minfo = info
        # Apply translation and rotation here

    def write(self, out):
        # Implementation of write goes here
        pass

    @staticmethod
    def normalizeMol(mol: pybel.Molecule):
        # Implementation of normalizeMol goes here
        pass

    @staticmethod
    def computeAndApplyNormalization(coords: List[np.ndarray], translate: np.ndarray, rotate: np.ndarray):
        # Implementation of computeAndApplyNormalization goes here
        pass