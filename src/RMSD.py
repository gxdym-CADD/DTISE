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

import numpy as np

class RMSDResult:
    def __init__(self, v=0.0, t=np.zeros(3), r=np.eye(3)):
        self.val = float(v)
        self.rotation = np.array(r, dtype=np.float32)
        self.translation = np.array(t, dtype=np.float32)

    def clear(self):
        self.val = 0.0
        self.rotation = np.eye(3, dtype=np.float32)
        self.translation = np.zeros(3, dtype=np.float32)

    def value(self):
        return self.val

    def setValue(self, v):
        self.val = float(v)

    def reorient(self, pnts):
        for i in range(len(pnts)):
            pnts[i] = np.dot(self.rotation, pnts[i]) + self.translation

    def reorient_coords(self, coords):
        n = len(coords) // 3
        pnts = np.array(coords).reshape(n, 3)
        self.reorient(pnts)
        return pnts.flatten()

    def reorient_mol(self, mol):
        coords = np.array(mol.GetCoordinates())
        new_coords = self.reorient_coords(coords)
        mol.SetCoordinates(new_coords)

    @property
    def rotationMatrix(self):
        return self.rotation

    @property
    def translationVector(self):
        return self.translation

def calculateRMSD(ref, fit, n):
    # Placeholder for actual RMSD calculation logic
    pass

def calculateRMSD_weighted(ref, fit, weights, n):
    # Placeholder for actual weighted RMSD calculation logic
    pass