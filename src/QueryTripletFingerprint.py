# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

"""
QueryTripletFingerprint.py

Created on: Nov 2, 2010
Author: dkoes

Checks to see if a fingerprint potentially matches the query
"""

from typing import List, Tuple
import TripletFingerprint
import SimpleFingers
import BitSetTree

class PharmerQuery:
    # Placeholder for PharmerQuery class
    pass

class QueryTripletFingerprint:
    # multi resolution search, first check bigqfingers (first DISTPACE), then if there is a match,
    # check corresponding smallqfingers (second DISTPACE)
    def __init__(self):
        assert TripletFingerprint.NUMDISTSPACES <= 2
        self.bigqfingers: List[List[TripletFingerprint]] = []  # all possible fingerprints of each query point not part of this triplet
        self.smallqfingers: List[List[List[TripletFingerprint]]] = []

    def set(self, i: int, j: int, k: int, query: PharmerQuery):
        pass

    def is_valid(self, f: TripletFingerprint) -> bool:
        return True

# Example usage
if __name__ == "__main__":
    # Placeholder for example usage
    pass