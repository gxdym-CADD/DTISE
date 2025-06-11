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
ShapeConstraints.py

Created on: Jun 11, 2012
Author: dkoes

This class is used to define an excluded space and is used to
check to see if any points fall within this space.
"""

import json
from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
from scipy.spatial.transform import Rotation as R

# Assuming PHARMIT_DIMENSION, PHARMIT_RESOLUTION, RMSDResult, PMol, MGrid, and OpenBabel are defined elsewhere
PHARMIT_DIMENSION = 100  # Example value
PHARMIT_RESOLUTION = 1.0  # Example value

@dataclass
class Sphere:
    x: float
    y: float
    z: float
    rSq: float

    def contains(self, a: float, b: float, c: float) -> bool:
        d1 = (a - self.x) ** 2
        d2 = (b - self.y) ** 2
        d3 = (c - self.z) ** 2
        distSq = d1 + d2 + d3
        return distSq <= self.rSq

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, r: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.rSq = r * r

class ShapeConstraints:
    probeRadius: float = 1.4  # Example value

    class Kind:
        None = 0
        Shape = 1
        Spheres = 2

    def __init__(self):
        self.exspheres: List[Sphere] = []
        self.inspheres: List[Sphere] = []

        self.excludeGrid = MGrid(PHARMIT_DIMENSION, PHARMIT_RESOLUTION)
        self.includeGrid = MGrid(PHARMIT_DIMENSION, PHARMIT_RESOLUTION)
        self.ligandGrid = MGrid(PHARMIT_DIMENSION, PHARMIT_RESOLUTION)

        self.inclusiveKind = ShapeConstraints.Kind.None
        self.exclusiveKind = ShapeConstraints.Kind.None

    def computeTransform(self, root: dict) -> np.ndarray:
        # Placeholder for transformation computation
        return np.eye(4)

    def makeGrid(self, grid: MGrid, mol: OpenBabel.OBMol, transform: np.ndarray, tolerance: float):
        # Placeholder for grid creation
        pass

    def getMesh(self, grid: MGrid, mesh: dict):
        # Placeholder for mesh retrieval
        pass

    def readJSONExclusion(self, root: dict) -> bool:
        # Placeholder for JSON reading
        return True

    def addToJSON(self, root: dict):
        # Placeholder for JSON writing
        pass

    def isExcluded(self, mol: PMol, res: RMSDResult) -> bool:
        # Placeholder for exclusion check
        return False

    @property
    def isDefined(self) -> bool:
        return self.inclusiveKind != ShapeConstraints.Kind.None or self.exclusiveKind != ShapeConstraints.Kind.None

    @property
    def isFullyDefined(self) -> bool:
        return self.inclusiveKind != ShapeConstraints.Kind.None and self.exclusiveKind != ShapeConstraints.Kind.None

    def isMeaningful(self) -> bool:
        # Placeholder for meaningful check
        return True

    def clear(self):
        self.exspheres.clear()
        self.inspheres.clear()

    def enableExclusionSpheres(self):
        self.exclusiveKind = ShapeConstraints.Kind.Spheres

    def addExclusionSphere(self, x: float, y: float, z: float, r: float):
        self.exspheres.append(Sphere(x, y, z, r))

    def enableInclusiveSpheres(self):
        self.inclusiveKind = ShapeConstraints.Kind.Spheres

    def addInclusiveSphere(self, x: float, y: float, z: float, r: float):
        self.inspheres.append(Sphere(x, y, z, r))

    @property
    def getExcludeGrid(self) -> MGrid:
        return self.excludeGrid

    @property
    def getIncludeGrid(self) -> MGrid:
        return self.includeGrid

    @property
    def getLigandGrid(self) -> MGrid:
        return self.ligandGrid

    @property
    def getGridTransform(self) -> np.ndarray:
        return self.gridtransform

    @staticmethod
    def computeInteractionPoints(ligand: OpenBabel.OBMol, receptor: OpenBabel.OBMol, points: List[np.ndarray]):
        # Placeholder for interaction point computation
        pass