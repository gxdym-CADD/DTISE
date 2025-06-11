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
SphereGrid.py

Representation of gridded points on a unit sphere.
Created on: May 6, 2010
Author: dkoes
"""

from typing import List, Tuple
import math
from openbabel import pybel, openbabel

class SphereGridPoint:
    def __init__(self, index: int = 0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.index = index
        self.neighbors: List[int] = []
        self.pnt = openbabel.vector3(x, y, z)

    def sqdistance(self, rhs: 'SphereGridPoint') -> float:
        return self.pnt.distSq(rhs.pnt)

class SphereGrid:
    SPHEREGRID_BITS = 5

    def __init__(self):
        # by default combine two platonic solids and get 32 points
        # not quite evenly spaced, but good enough
        self.points: List[SphereGridPoint] = []
        self.makeDodecahedron()
        self.makeIcosahedron()
        self.connectPoints()

    def addCoords(self, coords: List[openbabel.vector3]):
        for i, coord in enumerate(coords):
            self.points.append(SphereGridPoint(i, coord.x(), coord.y(), coord.z()))

    def makeDodecahedron(self):
        # 20 points
        pass

    def makeIcosahedron(self):
        # 12 points, dual of dodecahedron
        pass

    def connectPoints(self):
        # Connect the points to form a grid
        pass

    def pointToGrid(self, x: float, y: float, z: float) -> int:
        # Return a grid point (0..32)
        pass

    def searchMask(self, pt: int, angle: float) -> int:
        # Return a mask of all grid points within angle of pt
        pass

sphereGrid = SphereGrid()