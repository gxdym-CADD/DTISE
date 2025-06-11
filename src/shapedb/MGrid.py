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
MGrid.py

Created on: Nov 21, 2011
A class for representing a grid of molecular data.
Author: dkoes
"""

from typing import List, Tuple
import numpy as np
from bitarray import bitarray

class MGrid:
    def __init__(self, d: float = 32.0, r: float = 0.5):
        self.dimension = d
        self.resolution = r
        self.grid_size = int(d / r)
        self.grid = bitarray(self.grid_size ** 3)
        self.grid.setall(False)

    def gridToPoint(self, g: int) -> Tuple[float, float, float]:
        x = (g % self.grid_size) * self.resolution - self.dimension / 2
        y = ((g // self.grid_size) % self.grid_size) * self.resolution - self.dimension / 2
        z = (g // (self.grid_size ** 2)) * self.resolution - self.dimension / 2
        return x, y, z

    def pointToGrid(self, x: float, y: float, z: float) -> int:
        ix = int((x + self.dimension / 2) / self.resolution)
        iy = int((y + self.dimension / 2) / self.resolution)
        iz = int((z + self.dimension / 2) / self.resolution)
        if 0 <= ix < self.grid_size and 0 <= iy < self.grid_size and 0 <= iz < self.grid_size:
            return ix + iy * self.grid_size + iz * (self.grid_size ** 2)
        else:
            return -1

    def markZChord(self, x: float, y: float, z: float, r: float):
        pass  # Placeholder for actual implementation

    def markYZCircle(self, x: float, y: float, z: float, r: float):
        pass  # Placeholder for actual implementation

    def shrinkByOne(self):
        pass  # Placeholder for actual implementation

    def growByOne(self):
        pass  # Placeholder for actual implementation

    def makeFace(self, pt: np.ndarray, which: int, r: float,
                  vertices: List[np.ndarray], normals: List[np.ndarray], faces: List[int]):
        pass  # Placeholder for actual implementation

    def markXYZSphere(self, x: float, y: float, z: float, r: float):
        pass  # Placeholder for actual implementation

    def getResolution(self) -> float:
        return self.resolution

    def getDimension(self) -> float:
        return self.dimension

    def copyFrom(self, from_grid: 'MGrid'):
        assert self.dimension == from_grid.dimension and self.resolution == from_grid.resolution
        self.grid = from_grid.grid.copy()

    def test(self, x: float, y: float, z: float) -> bool:
        pt = self.pointToGrid(x, y, z)
        if pt >= 0:
            return self.grid[pt]
        else:
            return True

    def inGrid(self, x: float, y: float, z: float) -> bool:
        return self.pointToGrid(x, y, z) >= 0

    def containsPoint(self, x: float, y: float, z: float) -> bool:
        return self.test(x, y, z)

    def intersects(self, cube: 'Cube') -> bool:
        return True

    def setPoint(self, x: float, y: float, z: float):
        pt = self.pointToGrid(x, y, z)
        if pt >= 0:
            self.grid[pt] = True

    def makeSurface(self, sagrid: 'MGrid', probe: float):
        pass  # Placeholder for actual implementation

    def isInteriorPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def isExposedPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def isSolitaryPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def sphereToGridIndices(self, x: float, y: float, z: float, r: float):
        indices = []
        ix_min = max(0, int((x - r + self.dimension / 2) / self.resolution))
        ix_max = min(self.grid_size, int((x + r + self.dimension / 2) / self.resolution))
        iy_min = max(0, int((y - r + self.dimension / 2) / self.resolution))
        iy_max = min(self.grid_size, int((y + r + self.dimension / 2) / self.resolution))
        iz_min = max(0, int((z - r + self.dimension / 2) / self.resolution))
        iz_max = min(self.grid_size, int((z + r + self.dimension / 2) / self.resolution))

        for ix in range(ix_min, ix_max):
            for iy in range(iy_min, iy_max):
                for iz in range(iz_min, iz_max):
                    i = ix + iy * self.grid_size + iz * (self.grid_size ** 2)
                    if np.linalg.norm(np.array([x - self.gridToPoint(i)[0], y - self.gridToPoint(i)[1], z - self.gridToPoint(i)[2]])) <= r:
                        indices.append(i)
        return indices

    def makeFace(self, pt: np.ndarray, which: int, r: float,
                  vertices: List[np.ndarray], normals: List[np.ndarray], faces: List[int]):
        pass  # Placeholder for actual implementation

    def markXYZSphere(self, x: float, y: float, z: float, r: float):
        indices = self.sphereToGridIndices(x, y, z, r)
        for i in indices:
            self.grid[i] = True

    def getResolution(self) -> float:
        return self.resolution

    def getDimension(self) -> float:
        return self.dimension

    def copyFrom(self, from_grid: 'MGrid'):
        assert self.dimension == from_grid.dimension and self.resolution == from_grid.resolution
        self.grid = from_grid.grid.copy()

    def test(self, x: float, y: float, z: float) -> bool:
        pt = self.pointToGrid(x, y, z)
        if pt >= 0:
            return self.grid[pt]
        else:
            return True

    def inGrid(self, x: float, y: float, z: float) -> bool:
        return self.pointToGrid(x, y, z) >= 0

    def containsPoint(self, x: float, y: float, z: float) -> bool:
        return self.test(x, y, z)

    def intersects(self, cube: 'Cube') -> bool:
        return True

    def setPoint(self, x: float, y: float, z: float):
        pt = self.pointToGrid(x, y, z)
        if pt >= 0:
            self.grid[pt] = True

    def makeSurface(self, sagrid: 'MGrid', probe: float):
        pass  # Placeholder for actual implementation

    def isInteriorPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def isExposedPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def isSolitaryPoint(self, x: float, y: float, z: float) -> bool:
        pass  # Placeholder for actual implementation

    def shrinkByOne(self):
        pass  # Placeholder for actual implementation

    def growByOne(self):
        pass  # Placeholder for actual implementation