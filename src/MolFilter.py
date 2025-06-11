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
mol_filter.py

Created on: Jan 28, 2011
Author: dkoes
"""

from openbabel import pybel

# Base class for specifying to creator to skip certain mols
class MolFilter:
    def skip(self, mol):
        raise NotImplementedError("Subclasses should implement this!")

class WeightRangeFilter(MolFilter):
    def __init__(self, min_weight=0, max_weight=float('inf')):
        self.min = min_weight
        self.max = max_weight

    def badWeight(self, weight):
        if weight < self.min:
            return True
        if weight >= self.max:
            return True
        return False

    # Include min, not max
    def skip(self, mol):
        return self.badWeight(mol.molwt)