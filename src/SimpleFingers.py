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
SimpleFingers.py

Created on: Jan 14, 2011
Author: dkoes

Classes and routines for computing and manipulating triplet relative fingerprints
which is what I call a very coarse finger print of the entire molecule defined
relative to a specific triplet. The coarseness makes it more appropriate binning
molecule, although of course they will not be evenly distributed.
"""

from typing import List, Tuple
import bitarray

# for each bit in a simplefinger, precompute all the possible bitsets
class SimpleFingerCollection:
    def __init__(self, pharmas: List['Pharma']):
        self.pharmaStart = [0] * len(pharmas)
        self.checkIfSet: List[bitarray.bitarray] = []
        self.N = 0  # number of bits in SF
        self.set_pharmas(pharmas)

    def set_pharmas(self, pharmas: List['Pharma']):
        self.pharmaStart = [0] * len(pharmas)
        self.N = 0
        for i, pharma in enumerate(pharmas):
            self.pharmaStart[i] = self.N
            self.N += pharma.simpleFingerBits

        # store what numbers have each bit set for easy manipulation
        max_value = 1 << self.N
        self.checkIfSet = [bitarray.bitarray(max_value) for _ in range(max_value)]

        for i in range(max_value):
            for v in range(max_value):
                if (v & i):  # i overlaps v
                    self.checkIfSet[i][v] = True  # v is a collection we must consider for i

    def get_collections(self, b: int) -> bitarray.bitarray:
        assert b < len(self.checkIfSet)
        return self.checkIfSet[b]

    def num_bits(self) -> int:
        return self.N

    def num_collections(self) -> int:
        return 1 << self.N

    def get_pharma_start(self, p: 'Pharma') -> int:
        return self.pharmaStart[p.index]

# compute the fingerprint bit of a single point
def compute_simple_finger_bit(SFC: SimpleFingerCollection, p: 'Pharma', underplane: bool, dist: float) -> int:
    index = SFC.get_pharma_start(p)
    ret = 0
    match p.simpleFingerBits:
        case 0:
            return ret
        case 1:  # present/not present
            ret |= (1 << index)
        case 4:  # chiral/not chiral and in/out of radius
            # bit 0: underplane and long dist
            # bit 1: overplane and long dist
            # bit 3: short dist
            if dist <= p.simpleFingerRadius:
                ret |= (1 << (index + 2))
            elif underplane:
                ret |= (1 << index)
            else:
                ret |= (1 << (index + 1))
        case 2:  # chiral/not chiral
            if underplane:
                ret |= (1 << index)
            else:
                ret |= (1 << (index + 1))
        case _:
            raise ValueError("Invalid simpleFingerBits value")
    return ret

class SimpleFinger:
    def __init__(self, SFC: SimpleFingerCollection):
        self.SFC = SFC
        self.finalMask = bitarray.bitarray(SFC.num_collections())
        self.currMask = 0
        self.finalMask.setall(True)  # start all set since intersect between points

    # add one piece of data for a query point; these all get or'ed together until
    # finishpoint which will find an intersection
    def add_query_point_data(self, p: 'Pharma', underplane: bool, mindist: float, maxdist: float):
        self.currMask |= compute_simple_finger_bit(self.SFC, p, underplane, mindist)
        self.currMask |= compute_simple_finger_bit(self.SFC, p, underplane, maxdist)

class Pharma:
    def __init__(self, index: int, simpleFingerBits: int, simpleFingerRadius: float):
        self.index = index
        self.simpleFingerBits = simpleFingerBits
        self.simpleFingerRadius = simpleFingerRadius

# Example usage:
if __name__ == "__main__":
    pharmas = [
        Pharma(index=0, simpleFingerBits=2, simpleFingerRadius=1.5),
        Pharma(index=1, simpleFingerBits=3, simpleFingerRadius=2.0)
    ]
    SFC = SimpleFingerCollection(pharmas)
    sf = SimpleFinger(SFC)
    # Add query point data
    sf.add_query_point_data(pharmas[0], underplane=True, mindist=1.0, maxdist=3.0)
    sf.add_query_point_data(pharmas[1], underplane=False, mindist=2.5, maxdist=4.0)
class Pharma:
    def __init__(self, index, simpleFingerBits, simpleFingerRadius):
        self.index = index
        self.simpleFingerBits = simpleFingerBits
        self.simpleFingerRadius = simpleFingerRadius

class SimpleFingerCollection:
    def __init__(self, pharmas):
        self.pharmas = pharmas

    def getCollections(self, currMask):
        # Placeholder for actual implementation
        return set()

class SimpleFinger:
    def __init__(self, SFC):
        self.SFC = SFC
        self.currMask = 0
        self.finalMask = set()

    def add_query_point_data(self, p, underplane, mindist, maxdist):
        self.currMask |= self.compute_simple_finger_bit(p, underplane, mindist)
        self.currMask |= self.compute_simple_finger_bit(p, underplane, maxdist)

    def finish_point(self):
        self.finalMask &= self.SFC.getCollections(self.currMask)
        self.currMask = 0

    def get_collections(self):
        return self.finalMask

    def compute_simple_finger_bit(self, p, underplane, distance):
        # Placeholder for actual implementation
        return 1  # Example return value

# Example usage:
if __name__ == "__main__":
    pharmas = [
        Pharma(index=0, simpleFingerBits=2, simpleFingerRadius=1.5),
        Pharma(index=1, simpleFingerBits=3, simpleFingerRadius=2.0)
    ]
    SFC = SimpleFingerCollection(pharmas)
    sf = SimpleFinger(SFC)
    # Add query point data
    sf.add_query_point_data(pharmas[0], underplane=True, mindist=1.0, maxdist=3.0)
    sf.add_query_point_data(pharmas[1], underplane=False, mindist=2.5, maxdist=4.0)