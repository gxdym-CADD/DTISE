# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

from ShapeConstraints import ShapeConstraints
from pharmerdb import PharmerDatabaseSearcher
from Triplet import QueryTriplet, TripletMatches
from cors import CorAllocator, CorrespondenceResult
from MTQueue import MTQueue
from RMSD import calculateRMSD
from params import QueryParameters, PropFilter
import CommandLine2.CommandLine as cl

UnWeightedRMSD = cl.opt(bool)

class Corresponder:
    def __init__(self, dbptr: PharmerDatabaseSearcher, dbid: int, numdbids: int, points: list, triplets: list, inQ: TripletMatches, alloc: CorAllocator, threadQ: int, resultQ: MTQueue, qparams: QueryParameters, excluder: ShapeConstraints, stopEarly: bool):
        self.dbptr = dbptr
        self.dbid = dbid
        self.numdbids = numdbids
        self.points = points
        self.triplets = triplets
        self.inQ = inQ
        self.alloc = alloc
        self.threadQ = threadQ
        self.resultQ = resultQ
        self.qparams = qparams
        self.excluder = excluder

        self.tmpresult = CorrespondenceResult()
        self.tm = None  # current match being processed
        self.pointCoords = []
        self.weights = []
        self.molCoords = []  # coordinates of current match
        self.tmpCoords = []

        self.thisConfCnt = 0
        self.processedCnt = 0
        self.matchedCnt = 0

        self.stopEarly = stopEarly

    def isExcluded(self, result: CorrespondenceResult) -> bool:
        mdata = MolData()
        pread = PMolReaderSingleAlloc()
        self.dbptr.getMolData(self.tm.id, mdata, pread)

        return self.excluder.isExcluded(mdata.mol, result.rmsd)

    def generate(self, pos: int, alreadyMatched: int) -> bool:
        if pos < 0:  # base case
            assert len(self.pointCoords) == len(self.molCoords) and len(self.pointCoords) % 3 == 0
            n = len(self.weights)
            assert n == len(self.pointCoords) // 3

            if UnWeightedRMSD:
                self.tmpresult.rmsd = calculateRMSD(self.pointCoords, self.molCoords)
            else:
                self.tmpresult.rmsd = calculateRMSD_with_weights(self.pointCoords, self.molCoords, self.weights)

            if self.tmpresult.rmsd <= self.qparams.maxRMSD:
                goodprops = True
                for prop in self.qparams.propfilters:
                    val = self.dbptr.getMolProp(prop.kind, self.tmpresult.dbid)
                    if val < prop.min or val > prop.max:
                        goodprops = False
                        break

                if goodprops:
                    if not self.excluder.isDefined() or not self.isExcluded(self.tmpresult):
                        self.resultQ.push(self.alloc.newCorResult(self.tmpresult))
                        self.thisConfCnt += 1
                        if self.thisConfCnt >= self.qparams.orientationsPerConf:
                            return False  # terminate early

            return True
        else:
            one = 1
            trips = self.triplets[pos]
import numpy as np

class CorrespondenceResult:
    def __init__(self):
        self.cor = {}
        self.matchIndex = lambda index: self.cor.get(index, -1)
        self.setIndex = lambda index, value: self.cor.update({index: value})

class CorAllocator:
    def newCorResult(self):
        return CorrespondenceResult()

class MTQueue:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self, tm, threadQ):
        if self.queue:
            tm = self.queue.pop(0)
            return True
        return False

class TripletMatchInfo:
    def __init__(self, whichTripOrder, indices, coords):
        self.whichTripOrder = whichTripOrder
        self.indices = indices
        self.coords = coords

class Triplet:
    def __init__(self, points):
        self.points = points

    def getPoints(self):
        return self.points

class Point:
    def __init__(self, index, point, radiusWeight):
        self.index = index
        self.point = point
        self.radiusWeight = lambda: radiusWeight

class QueryTriplet:
    pass

class TripletMatches:
    def __init__(self, matches):
        self.matches = matches

class ShapeConstraints:
    def isDefined(self):
        return False

    def isExcluded(self, tmpresult):
        return False

class QueryParameters:
    def __init__(self, orientationsPerConf):
        self.orientationsPerConf = orientationsPerConf

class PharmerDatabaseSearcher:
    pass

class Corresponder:
    def __init__(self, dptr, dbid_, ndbids, pts, trips, m, ca, t, Q, qp, ex, stop):
        self.dbptr = dptr
        self.dbid = dbid_
        self.numdbids = ndbids
        self.points = pts
        self.triplets = trips
        self.inQ = m
        self.alloc = ca
        self.threadQ = t
        self.resultQ = Q
        self.qparams = qp
        self.excluder = ex
        self.tmpresult = self.alloc.newCorResult()
        self.tm = None
        self.thisConfCnt = 0
        self.processedCnt = 0
        self.matchedCnt = 0
        self.stopEarly = stop
        self.pointCoords = []
        self.molCoords = []
        self.weights = []

    def generate(self, pos, alreadyMatched):
        if pos < 0:
            return True
        else:
            one = 1
            trips = self.triplets[pos]
            for i in range(len(self.tm.matches[pos])):
                info = self.tm.matches[pos][i]
                trip = trips[info.whichTripOrder]
                newqpoints = [-1, -1, -1]
                newmpoints = [-1, -1, -1]
                valid = True
                for j in range(3):
                    if newmpoints.count(info.indices[j]) > 0:
                        valid = False
                        break
                    newmpoints[j] = info.indices[j]
                    newqpoints[j] = trip.getPoints()[j].index

                if not valid:
                    continue

                alreadyMatched |= (1 << newmpoints[0])
                alreadyMatched |= (1 << newmpoints[1])
                alreadyMatched |= (1 << newmpoints[2])

                for j in range(3):
                    self.tmpresult.setIndex(newqpoints[j], newmpoints[j])

                if not self.generate(pos - 1, alreadyMatched):
                    return False

                alreadyMatched &= ~(1 << newmpoints[0])
                alreadyMatched &= ~(1 << newmpoints[1])
                alreadyMatched &= ~(1 << newmpoints[2])

            return True

    def __call__(self):
        self.tm = None
        while self.inQ.pop(self.tm, self.threadQ):
            if self.stopEarly:
                break
            self.tmpresult.reinitialize(self.tm, self.dbid, self.numdbids)
            self.thisConfCnt = 0
            self.processedCnt += 1
            if not self.generate(len(self.triplets) - 1, 0):
                self.pointCoords.clear()
                self.molCoords.clear()
                self.weights.clear()
            if self.thisConfCnt > 0:
                self.matchedCnt += 1

        self.resultQ.removeProducer()

        if not Quiet:
            print(f"Correspondence ProccessedCnt {self.processedCnt} MatchedCnt {self.matchedCnt} ({100 * (self.matchedCnt / self.processedCnt):.2f}%)")

# Example usage
if __name__ == "__main__":
    # Initialize necessary components and parameters
    dptr = PharmerDatabaseSearcher()
    dbid_ = 1
    ndbids = 10
    pts = [Point(0, np.array([0, 0, 0]), 1), Point(1, np.array([1, 0, 0]), 1)]
    trips = [[Triplet(pts)], [Triplet(pts)]]
    m = TripletMatches([])
    ca = CorAllocator()
    t = MTQueue(0)
    Q = MTQueue(0)
    qp = QueryParameters(orientationsPerConf=10)
    ex = ShapeConstraints()
    stop = False

    # Create and run the Correspondence
    correspondencer = Corresponder(dptr, dbid_, ndbids, pts, trips, m, ca, t, Q, qp, ex, stop)
    correspondencer()