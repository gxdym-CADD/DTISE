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
Triplet.py

Created on: Aug 5, 2010
Author: dkoes

Three points make a triplet. Has a canonical form.
"""

from typing import List, Tuple
from collections import namedtuple
import numpy as np

# Convenience class for dealing with indexed pharma points
PharmaIndex = namedtuple('PharmaIndex', ['point', 'index', 'pharma_index'])

class TripletRange:
    def __init__(self):
        self.min: int = 0
        self.max: int = 0
        self.length: int = 0

class Triplet:
    DupKind = {
        'AllDifferent': 0,
        'FirstTwoSame': 1,
        'LastTwoSame': 2,
        'AllSame': 3
    }

    def __init__(self):
        self.PIs: List[PharmaIndex] = [None, None, None]
        self.range: List[TripletRange] = [TripletRange(), TripletRange(), TripletRange()]
        self.nextUnconnectIndex: int = 0
        self.prevUnconnectIndex: int = 0
        self.kind: str = 'AllDifferent'

    def computeLengths(self):
        self.range[0].length = ThreePointData.reduceFloatUnsigned(
            PharmaPoint.pharmaDist(self.PIs[0].point, self.PIs[1].point))
        self.range[1].length = ThreePointData.reduceFloatUnsigned(
            PharmaPoint.pharmaDist(self.PIs[1].point, self.PIs[2].point))
        self.range[2].length = ThreePointData.reduceFloatUnsigned(
            PharmaPoint.pharmaDist(self.PIs[2].point, self.PIs[0].point))

        # Mins
        self.range[0].min = 0
        self.range[1].min = 0
        self.range[2].min = 0

        dist = ThreePointData.reduceFloatUnsigned(
            self.PIs[0].point.radius + self.PIs[1].point.radius)
        if dist < self.range[0].length:
            self.range[0].min = dist

        dist = ThreePointData.reduceFloatUnsigned(
            self.PIs[1].point.radius + self.PIs[2].point.radius)
        if dist < self.range[1].length:
            self.range[1].min = dist

        dist = ThreePointData.reduceFloatUnsigned(
            self.PIs[2].point.radius + self.PIs[0].point.radius)
        if dist < self.range[2].length:
            self.range[2].min = dist

        # Maxs
        self.range[0].max = np.inf
        self.range[1].max = np.inf
        self.range[2].max = np.inf

    def swap(self, i: int, j: int):
        self.PIs[i], self.PIs[j] = self.PIs[j], self.PIs[i]

        if self.nextUnconnectIndex == i:
            self.nextUnconnectIndex = j
        elif self.nextUnconnectIndex == j:
            self.nextUnconnectIndex = i

        if self.prevUnconnectIndex == i:
            self.prevUnconnectIndex = j
        elif self.prevUnconnectIndex == j:
            self.prevUnconnectIndex = i

        if i == 0:
            if j == 1:
                self.range[1], self.range[2] = self.range[2], self.range[1]
            elif j == 2:
                self.range[0], self.range[1] = self.range[1], self.range[0]
        elif i == 1:
            if j == 0:
                self.range[1], self.range[2] = self.range[2], self.range[1]
            elif j == 2:
                self.range[0], self.range[2] = self.range[2], self.range[0]
        elif i == 2:
            if j == 0:
                self.range[0], self.range[1] = self.range[1], self.range[0]
            elif j == 1:
                self.range[0], self.range[2] = self.range[2], self.range[0]

    def canonize(self):
        # 4 cases
        # all different kinds
        if (self.PIs[0].pharma_index != self.PIs[1].pharma_index and
            self.PIs[0].pharma_index != self.PIs[2].pharma_index and
            self.PIs[1].pharma_index != self.PIs[2].pharma_index):
            # use the current order, it's fully constrained
            self.kind = 'AllDifferent'
        # all the same kind
        elif (self.PIs[0].pharma_index == self.PIs[1].pharma_index and
              self.PIs[1].pharma_index == self.PIs[2].pharma_index):
            self.kind = 'AllSame'
class Triplet:
    def __init__(self, pis=None, r=None, nc=0, pc=0):
        if pis is not None and r is not None:
            self.PIs = pis
            self.range = r
            self.nextUnconnectIndex = nc
            self.prevUnconnectIndex = pc
        else:
            self.PIs = [None] * 3
            self.range = [None] * 3
            self.nextUnconnectIndex = 0
            self.prevUnconnectIndex = 0

    def sort(self):
        # Sort PIs based on pharma_index
        self.PIs.sort(key=lambda x: x.pharma_index)

    def computeLengths(self):
        # Placeholder for computing lengths
        pass

    def canonize(self):
        if (self.PIs[0].pharma_index != self.PIs[1].pharma_index and
                self.PIs[0].pharma_index != self.PIs[2].pharma_index and
                self.PIs[1].pharma_index != self.PIs[2].pharma_index):
            # use the current order, it's fully constrained
            self.kind = 'AllDifferent'
        # all the same kind
        elif (self.PIs[0].pharma_index == self.PIs[1].pharma_index and
                self.PIs[0].pharma_index == self.PIs[2].pharma_index):
            self.kind = 'AllSame'
            if self.range[0].length < self.range[1].length:
                self.swap(0, 1)
            if self.range[0].length < self.range[2].length:
                self.swap(0, 2)
            if self.range[1].length > self.range[2].length:
                self.swap(1, 2)

    def swap(self, i, j):
        self.PIs[i], self.PIs[j] = self.PIs[j], self.PIs[i]
        self.range[i], self.range[j] = self.range[j], self.range[i]

    def setNextUnconnected(self, k):
        self.nextUnconnectIndex = k

    def getV(self):
        ret = 1.0
        for i in range(3):
            ret *= ThreePointData.unreduceFloat(self.range[i].max - self.range[i].min)
        return ret

    def getNextUnconnected(self):
        return self.nextUnconnectIndex

    def getPrevUnconnected(self):
        return self.prevUnconnectIndex

    def getPoints(self):
        return self.PIs

    def getRanges(self):
        return self.range

    def getPharma(self, p):
        return self.PIs[p].point.pharma.index

    def dump(self):
        for i in range(3):
            print(f"{self.PIs[i].index} {self.PIs[i].pharmaIndex} "
                  f"{self.range[i].length} {self.range[i].min} "
                  f"{self.range[i].max} | ", end="")
        print(f"N{self.nextUnconnectIndex} P{self.prevUnconnectIndex}")

class QueryTriplet(Triplet):
    def __init__(self, pis=None, r=None, nc=0, pc=0):
        super().__init__(pis, r, nc, pc)
        self.mybox = BoundingBox()
        self.ref = [0.0] * 9
        self.a, self.b, self.c = 0.0, 0.0, 0.0
        self.aang, self.bang, self.cang = 0.0, 0.0, 0.0
        self.r0, self.r1, self.r2 = 0.0, 0.0, 0.0
        self.smallAthresholdsmallB = 0.0
        self.smallAthresholdlargeB = 0.0
        self.smallAthresholdlargeC = 0.0
        self.largeCthresholdsmallA = 0.0
        self.lengths = [0.0] * 3
        self.angles = [0.0] * 3
        self.radii = [0.0] * 3
        self.tangd = [0.0] * 3
        self.tangdM = [0.0] * 3
        self.smallLowerThresholds = [[0.0] * 3 for _ in range(3)]
        self.smallUpperThresholds = [[0.0] * 3 for _ in range(3)]
        self.largeLowerThresholds = [[0.0] * 3 for _ in range(3)]
        self.largeUpperThresholds = [[0.0] * 3 for _ in range(3)]
        self.fingerprint = QueryTripletFingerprint()
class QueryTriplet:
    def __init__(self):
        self.geCthresholdsmallA = 0.0
        self.lengths = [0.0] * 3
        self.angles = [0.0] * 3
        self.radii = [0.0] * 3
        self.tangd = [0.0] * 3
        self.tangdM = [0.0] * 3
        self.smallLowerThresholds = [[0.0] * 3 for _ in range(3)]
        self.smallUpperThresholds = [[0.0] * 3 for _ in range(3)]
        self.bigLowerThresholds = [[0.0] * 3 for _ in range(3)]
        self.bigUpperThresholds = [[0.0] * 3 for _ in range(3)]
        self.fingerprint = [0] * 256
        self.mybox = None
        self.range = None
        self.PI = 3.141592653589793
        self.PISQR = 9.869604401089358
        self.TWOPI = 6.283185307179586
        self.PITRIPLE = 9.42477796076938
        self.PIHALF = 1.5707963267948966
        self.PISIXTH = 0.5235987755982988
        self.PI23RD = 2.0943951023931953
        self.PI45TH = 2.6179938779914944
        self.PISIXTHSQ = 0.2748893571891065
        self.EPSILON = 1e-7
        self.fingerprintSize = 256
        self.searchDataComputed = False
        self.fingerprintComputed = False
        self.PIsixthcubed = 0.02443460952792061
        self.PIhalfsqr = 2.4674011002723395
        self.fingerprintScale = 512.0

    def set_extra(self, point, min_size, max_size, vector_mask):
        # Implement the logic for setting extra data here
        pass

    def compute_search_data(self):
        self.set_extras()
        self.mybox.minx = self.range[0].min
        self.mybox.maxx = self.range[0].max
        # Implement the rest of the logic for computing search data here

    def compute_tang_d_min(self, ra, rb, ab, theta, ac):
        t1 = ra - rb
        t3 = 1.0 / ab
        t4 = t3 * t1 * ra
        t8 = ab + t3 * t1 * rb - t4
        t10 = (t1 * t1)
        t11 = ab * ab
        t12 = 1.0 / t11
        t15 = (1 - t12 * t10) ** 0.5
        t16 = t15 * ra
        t19 = t15 * rb - t16
        t22 = (t8 * (x3 - t4) + t19 * (y3 - t16)) * t12
        x = t4 + t8 * t22
        t25 = x3 - x
        y = t16 + t19 * t22
        t28 = y3 - y
        a = math.atan2(t28, t25)
        x2 = y / math.tan(a)
        ddist = (x2 * x2 + y * y) ** 0.5
        cdist = ((x3 - x + x2) * (x3 - x + x2) + y3 * y3) ** 0.5
        if cdist < ddist:
            return 0
        t25 *= t25
        t28 *= t28
        d = (t25 + t28) ** 0.5
        return d

    def compute_tang_d_max(self, ra, rb, ab, theta, ac):
        t1 = ra - rb
        t3 = 1.0 / ab
        t4 = t3 * t1 * ra
        t8 = ab + t3 * t1 * rb - t4
        t10 = (t1 * t1)
        t11 = ab * ab
        t12 = 1.0 / t11
        t15 = (1 - t12 * t10) ** 0.5
        t16 = t15 * ra
        t19 = t15 * rb - t16
        t22 = (t8 * (x3 - t4) + t19 * (y3 - t16)) * t12
        x = t4 + t8 * t22
        y = t16 + t19 * t22
        d = ((x3 - x) ** 2 + y * y) ** 0.5
        return d

# Example usage:
# query_point = QueryPoint()
# query_point.compute_search_data()
import math

def compute_search_data(query_point):
    set_extras()

    query_point.mybox.minx = query_point.range[0].min
    query_point.mybox.maxx = query_point.range[0].max
    query_point.mybox.miny = query_point.range[1].min
    query_point.mybox.maxy = query_point.range[1].max
    query_point.mybox.minz = query_point.range[2].min
    query_point.mybox.maxz = query_point.range[2].max

    for i in range(3):
        query_point.ref[i] = query_point.PIs[i].index

    query_point.aang = math.acos((query_point.distances[0]**2 + query_point.distances[1]**2 - query_point.distances[2]**2) / 
                                (2 * query_point.distances[0] * query_point.distances[1]))
    query_point.bang = math.acos((query_point.distances[0]**2 + query_point.distances[2]**2 - query_point.distances[1]**2) / 
                                (2 * query_point.distances[0] * query_point.distances[2]))
    query_point.cang = math.acos((query_point.distances[1]**2 + query_point.distances[2]**2 - query_point.distances[0]**2) / 
                                (2 * query_point.distances[1] * query_point.distances[2]))

    query_point.minkdistsq = min(query_point.distances)
    query_point.maxkdistsq = max(query_point.distances)

    for i in range(3):
        if query_point.skipfingers[i]:
            continue
        query_point.fingerprint.set(query_point.PIs[i].index, query_point.query)

def distance_k_too_large_for_ij(query_point, i, Li, j, Lj, k, Lk):
    d = query_point.tangd[query_point.sharedR[i][j]]
    if d <= 0:
        return False

    maxk = math.sqrt(Li**2 - d**2) + math.sqrt(Lj**2 - d**2)
    if Lk > maxk:
        return True

    rc = query_point.radii[query_point.sharedR[i][j]]
    # Additional checks can be added here based on the original code logic
    return False

# Example usage
class QueryPoint:
    def __init__(self, PIs, range, nc, pc):
        self.PIs = PIs
        self.range = range
        self.nc = nc
        self.pc = pc
        self.mybox = Box()
        self.ref = [0, 0, 0]
        self.distances = [0.0, 0.0, 0.0]
        self.aang = 0.0
        self.bang = 0.0
        self.cang = 0.0
        self.minkdistsq = 0.0
        self.maxkdistsq = 0.0
        self.skipfingers = [False, False, False]
        self.tangd = [0.0, 0.0, 0.0]
        self.radii = [0.0, 0.0, 0.0]
        self.sharedR = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
        self.fingerprint = Fingerprint()

class Box:
    def __init__(self):
        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0
        self.minz = 0
        self.maxz = 0

class Fingerprint:
    def set(self, index1, index2, index3, query):
        # Implement fingerprint setting logic here
        pass

# Example initialization and usage
query_point = QueryPoint([PharmaIndex(), PharmaIndex(), PharmaIndex()], [TripletRange(), TripletRange(), TripletRange()], 0, 0)
compute_search_data(query_point)

i, Li, j, Lj, k, Lk = 0, 1.0, 1, 2.0, 2, 3.0
result = distance_k_too_large_for_ij(query_point, i, Li, j, Lj, k, Lk)
print(result)
import math

class QueryPoint:
    def __init__(self, indices, ranges, minz, maxz):
        self.indices = indices
        self.ranges = ranges
        self.minz = minz
        self.maxz = maxz

def compute_search_data(query_point):
    # Implement search data computation logic here
    pass

def distance_k_too_large_for_ij(query_point, i, Li, j, Lj, k, Lk):
    # Assuming sharedR, lengths, radii, angles are attributes of query_point
    sharedR = query_point.sharedR
    lengths = query_point.lengths
    radii = query_point.radii
    angles = query_point.angles

    d = query_point.tangdM[sharedR[i][j]]
    if Li < d or Lj < d:
        return False  # j is not too large for i

    rc = math.sqrt(Li * Li + lengths[i] * lengths[i])
    if rc < 1e-6:
        return True  # Avoid division by zero

    if Lk > lengths[k]:
        return True  # k is too large

    d2 = (Li - lengths[i]) / rc
    if abs(d2) > 1:
        return True  # d2 out of bounds for acos

    theta = math.acos(d2)
    phi = angles[sharedA[i][j]]
    if not math.isfinite(phi):
        return False  # phi is not finite

    cos_phi_theta = math.cos(phi + theta)
    if cos_phi_theta < -1:
        cos_phi_theta = -1  # Clamp to valid range for acos
    elif cos_phi_theta > 1:
        cos_phi_theta = 1

    alpha = math.acos(cos_phi_theta) * lengths[k] / rc
    return Lk > alpha  # k is too large

# Additional functions can be implemented similarly, following the same structure and logic.
import math

def distancejTooLargeForLargei(i, Li, j, Lj, largeUpperThresholds, angles, radii, sharedA, unsharedR, lengths, rc):
    if Li >= largeUpperThresholds[i][j]:
        A = angles[sharedA[i][j]]
        iR = radii[unsharedR[i][j]]
        jR = radii[unsharedR[j][i]]
        l = Li - iR
        l2 = Lj - jR
        if l > 0 and l2 > 0 and math.isfinite(A):
            sR = radii[sharedR[i][j]]
            iL = lengths[i]
            jL = lengths[j]
            max_val = -2 * math.cos(2 * math.pi - math.acos(0.5 * (-l * l + iL * iL + sR * sR) / (iL * sR)) - A) * jL * sR + jL * jL + sR * sR
            if l2 * l2 > max_val:
                return True
    return False

def distancesTooLargeForSmallA(L1, L2, threshold, r0, r1, cang):
    if L1 < threshold:
        l = L1 + r0
        l2 = L2 - r1
        max_val = 2.0 * b * r1 * math.cos(cang + math.acos((-l * l + a * a + r1 * r1) / a / r1 / 2.0))
        if l2 * l2 > max_val:
            return True
    return False

def distancesTooLargeForSmallB(L1, L3, threshold, r1, r2, bang):
    if L1 < threshold:
        l = L1 + r1
        l2 = L3 - r2
        max_val = 2.0 * c * r0 * math.cos(bang + math.acos((-l * l + a * a + r0 * r0) / a / r0 / 2.0))
        if l2 * l2 > max_val:
            return True
    return False

class QueryTriplet(Triplet):
    def __init__(self, points=None, i=None, j=None, k=None):
        super().__init__(points, i, j, k)
        self.skipfingers = False
        if points is not None and i is not None and j is not None and k is not None:
            self.computeSearchData()

    def __del__(self):
        pass

    def getFingerPrint(self):
        return self.fingerprint

    def validOverlap(self):
        if self.kind == 'AllDifferent':
            return True
        elif self.kind == 'AllSame':
            return (self.range[0].min < self.range[1].max and 
                    self.range[1].min < self.range[2].max)
        elif self.kind == 'FirstTwoSame':
            return self.range[0].min < self.range[1].max
        elif self.kind == 'LastTwoSame':
            return self.range[1].min < self.range[2].max
        return False

    def numOrderings(self):
        if self.kind == 'AllDifferent':
            return 1
        elif self.kind == 'AllSame':
            return 6
        elif self.kind in ['FirstTwoSame', 'LastTwoSame']:
            return 2
        return 1

    def expand(self, result, query):
        tmp = QueryTriplet(*self)
        result.clear()
        result.reserve(6)
        tmp.canonize()
        result.append(tmp)

        if self.kind == 'AllDifferent':
            pass
        elif self.kind == 'AllSame':
            tmp.swap(1, 2)  # 132
            if tmp.validOverlap():
                result.push_back(tmp)

            tmp.swap(0, 2)  # 231
            if tmp.validOverlap():
                result.push_back(tmp)
class QueryTriplet:
    def __init__(self, *args):
        self.args = args

    def canonize(self):
        # Implement canonization logic here
        pass

    def swap(self, i, j):
        self.args[i], self.args[j] = self.args[j], self.args[i]

    def validOverlap(self):
        # Implement valid overlap logic here
        return True

    def setFingerPrints(self, query):
        # Implement setting fingerprints logic here
        pass

    def setExtras(self):
        # Implement setting extras logic here
        pass

class BoundingBox:
    def __init__(self, minx, maxx, miny, maxy, minz, maxz):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz

    def hasOverlap(self, other):
        # Implement overlap logic here
        return True

    def containedIn(self, other):
        # Implement containment logic here
        return True

class ThreePointData:
    @staticmethod
    def unreduceFloat(value):
        # Implement unreduction logic here
        return value

    def x1(self):
        # Implement x1 logic here
        return 0.0

    def y1(self):
        # Implement y1 logic here
        return 0.0

    def z1(self):
        # Implement z1 logic here
        return 0.0

class TripletManager:
    def __init__(self, *args):
        self.args = args

    def expand(self, query):
        result = []
        for i in range(len(query)):
            if query[i] == 'X':
                for j in range(1, 21):  # Assuming 20 possible values
                    new_query = list(query)
                    new_query[i] = str(j)
                    result.append(''.join(new_query))
            else:
                result.append(query)
        return result

    def get_matches(self, query):
        expanded_queries = self.expand(query)
        matches = []
        for q in expanded_queries:
            if self.matches(q):
                matches.append(q)
        return matches

    def matches(self, query):
        # Implement matching logic here
        return True

class TripletMatcher:
    def __init__(self, triplet_manager):
        self.triplet_manager = triplet_manager

    def find_matches(self, query):
        return self.triplet_manager.get_matches(query)

# Example usage
triplet_manager = TripletManager()
matcher = TripletMatcher(triplet_manager)
query = "1X3"
matches = matcher.find_matches(query)
print(matches)
import math
from typing import List, Tuple

class ThreePointData:
    @staticmethod
    def unreduceFloat(value: float) -> float:
        # Implement unreduce logic here
        return value

class RMSDResult:
    def __init__(self):
        self.data = []

    def reorient(self, n: int, a: List[float]) -> None:
        # Implement reorientation logic here
        pass

def calculateRMSD(b: List[float], a: List[float], n: int) -> RMSDResult:
    # Implement RMSD calculation logic here
    return RMSDResult()

class PharmaPoint:
    def __init__(self, x: float, y: float, z: float, radius: float):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    @staticmethod
    def pharmaDist(p1, p2) -> float:
        # Implement distance calculation logic here
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

class TripletMatcher:
    def __init__(self, triplet_manager):
        self.triplet_manager = triplet_manager

    def find_matches(self, query):
        return self.triplet_manager.get_matches(query)

# Example usage
triplet_manager = TripletManager()
matcher = TripletMatcher(triplet_manager)
query = "1X3"
matches = matcher.find_matches(query)
print(matches)

class Triplet:
    def __init__(self):
        self.PIs = []
        self.range = [(0, 0), (0, 0), (0, 0)]
        self.hasExtra = False
        self.minSize = [0, 0, 0]
        self.maxSize = [0, 0, 0]
        self.vectorMask = [False, False, False]
        self.skipfingers = False
        self.fingerprint = None
        self.prevUnconnectIndex = -1
        self.minkdistsq = []
        self.maxkdistsq = []

    def rmsdMatch(self, tdata: ThreePointData) -> bool:
        a = [0] * 9
        b = [0] * 9

        a[0], a[1], a[2] = ThreePointData.unreduceFloat(tdata.x1()), ThreePointData.unreduceFloat(tdata.y1()), ThreePointData.unreduceFloat(tdata.z1())
        a[3], a[4], a[5] = ThreePointData.unreduceFloat(tdata.x2()), ThreePointData.unreduceFloat(tdata.y2()), ThreePointData.unreduceFloat(tdata.z2())
        a[6], a[7], a[8] = ThreePointData.unreduceFloat(tdata.x3()), ThreePointData.unreduceFloat(tdata.y3()), ThreePointData.unreduceFloat(tdata.z3())

        b[0], b[1], b[2] = self.PIs[0].point.x, self.PIs[0].point.y, self.PIs[0].point.z
        b[3], b[4], b[5] = self.PIs[1].point.x, self.PIs[1].point.y, self.PIs[1].point.z
        b[6], b[7], b[8] = self.PIs[2].point.x, self.PIs[2].point.y, self.PIs[2].point.z

        r = calculateRMSD(b, a, 3)
        r.reorient(3, a)

        for i in range(9):
            if not math.isclose(a[i], b[i]):
                return False

        return True

    def is_good_k_distance(self, kdist: int, distback: int) -> bool:
        if len(self.minkdistsq) <= distback:
            return True
        return kdist >= self.minkdistsq[distback] and kdist <= self.maxkdistsq[distback]

    def set_skip_fingers(self, val: bool) -> None:
        self.skipfingers = val

class TripletManager:
    def get_matches(self, query):
        # Implement logic to find matches based on the query
        return []

# Example usage
triplet_manager = TripletManager()
matcher = TripletMatcher(triplet_manager)
query = "1X3"
matches = matcher.find_matches(query)
print(matches)