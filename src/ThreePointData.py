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
ThreePointData.py

Created on: Aug 6, 2010
Author: dkoes
"""

from typing import List, Tuple
import math
from pharmarec import PharmaPoint
from TripletFingerprint import TripletFingerprint
from SimpleFingers import SimpleFingers

TPD_MOLID_BITS = 24
TPD_MOLDATA_BITS = 40
TPD_LENGTH_BITS = 16
TPD_COORD_BITS = 16
TPD_ANGLE_BITS = 16
TPD_INDEX_BITS = 8
EXTRA_BITS = 6
WEIGHT_BITS = 10
ROTATABLE_BITS = 4

class ThreePointData:
    def __init__(self, offset: int, w: float, numrot: int, points: List[PharmaPoint], i: int, j: int, k: int):
        self.molPos: int = (offset << (TPD_MOLDATA_BITS - TPD_MOLID_BITS))
        self.i1: int = i
        self.i2: int = j
        self.i3: int = k
        self.l1: int = self.reduceFloat(points[j].dist(points[i]))
        self.l2: int = self.reduceFloat(points[k].dist(points[j]))
        self.l3: int = self.reduceFloat(points[i].dist(points[k]))
        self.x: int = self.reduceFloat(points[i].x)
        self.y: int = self.reduceFloat(points[i].y)
        self.z: int = self.reduceFloat(points[i].z)
        theta2, phi2 = self.spherical_coords(points[j], points[i])
        self.theta2: int = self.reduceAngle(theta2)
        self.phi2: int = self.reduceAngle(phi2)
        theta3, phi3 = self.spherical_coords(points[k], points[i])
        self.theta3: int = self.reduceAngle(theta3)
        self.phi3: int = self.reduceAngle(phi3)
        self.extra1: int = 0
        self.extra2: int = 0
        self.extra3: int = 0
        self.weight: int = self.reduceWeight(w)
        self.nrot: int = self.reduceRotatable(numrot)
        self.fingerprint: TripletFingerprint = TripletFingerprint()

    def __init__(self):
        self.molPos: int = 0
        self.i1: int = 0
        self.i2: int = 0
        self.i3: int = 0
        self.l1: int = 0
        self.l2: int = 0
        self.l3: int = 0
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.theta2: int = 0
        self.phi2: int = 0
        self.theta3: int = 0
        self.phi3: int = 0
        self.extra1: int = 0
        self.extra2: int = 0
        self.extra3: int = 0
        self.weight: int = 0
        self.nrot: int = 0
        self.fingerprint: TripletFingerprint = TripletFingerprint()

    def __init__(self, val: int):
        # Assuming this is a placeholder for some initialization logic
        pass

    @staticmethod
    def reduceAngle(angle: float) -> int:
        return int((angle / (2 * math.pi)) * (1 << TPD_ANGLE_BITS))

    @staticmethod
    def reduceFloat(value: float) -> int:
        max_value = 1 << TPD_COORD_BITS
        min_value = -max_value
        if value > max_value:
            return max_value
        elif value < min_value:
            return min_value
        return int((value / max_value) * (1 << TPD_COORD_BITS))

    @staticmethod
    def reduceWeight(weight: float) -> int:
        max_weight = 1 << WEIGHT_BITS
        if weight > max_weight:
            return max_weight
        elif weight < 0:
            return 0
        return int((weight / max_weight) * (1 << WEIGHT_BITS))

    @staticmethod
    def reduceRotatable(numrot: int) -> int:
        max_rotatable = 1 << ROTATABLE_BITS
        if numrot > max_rotatable:
            return max_rotatable
        elif numrot < 0:
            return 0
        return numrot

    @staticmethod
    def spherical_coords(p2: PharmaPoint, p1: PharmaPoint) -> Tuple[float, float]:
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dz = p2.z - p1.z
        r = math.sqrt(dx**2 + dy**2 + dz**2)
        theta = math.acos(dz / r)
        phi = math.atan2(dy, dx)
        return theta, phi

    def unpackMolID(self) -> int:
        return self.molPos >> (TPD_MOLDATA_BITS - TPD_MOLID_BITS)

    def x3(self) -> int:
        return round(self.x + self.l3 * math.cos(self.unreduceAngle(self.theta3)) * math.sin(self.unreduceAngle(self.phi3)))

    def y3(self) -> int:
        return round(self.y + self.l3 * math.sin(self.unreduceAngle(self.theta3)) * math.sin(self.unreduceAngle(self.phi3)))

    def z3(self) -> int:
        return round(self.z + self.l3 * math.cos(self.unreduceAngle(self.phi3)))

    @staticmethod
    def unreduceAngle(angle: int) -> float:
        return (angle / (1 << TPD_ANGLE_BITS)) * 2 * math.pi

# Assuming the countRotatableBonds function is defined elsewhere
def countRotatableBonds(mol):
    pass