import numpy as np

class PointCoords:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.z < other.z

    def maximize(self):
        self.x = np.iinfo(np.int16).max
        self.y = np.iinfo(np.int16).max
        self.z = np.iinfo(np.int16).max

    def distSQ(self, other):
        X = other.x - self.x
        Y = other.y - self.y
        Z = other.z - self.z
        return X * X + Y * Y + Z * Z

class TripletMatchInfo:
    def __init__(self, tdata=None, which=0, uncon=0, puncon=0):
        self.coords = [PointCoords(), PointCoords(), PointCoords()]
        self.indices = [0, 0, 0]
        self.whichTripOrder = which
        self.unconnectedNextIndex = uncon
        self.unconnectedPrevIndex = puncon

        if tdata is not None:
            self.coords[0] = PointCoords(tdata.x1(), tdata.y1(), tdata.z1())
            self.coords[1] = PointCoords(tdata.x2(), tdata.y2(), tdata.z2())
            self.coords[2] = PointCoords(tdata.x3(), tdata.y3(), tdata.z3())
            self.indices[0] = tdata.i1
            self.indices[1] = tdata.i2
            self.indices[2] = tdata.i3

    def dump(self):
        print(f"( {self.whichTripOrder},{self.unconnectedNextIndex} - ", end="")
        for i in range(3):
            print(f"{self.indices[i]} : {self.coords[i].x},{self.coords[i].y},{self.coords[i].z}", end="  ; " if i != 2 else "")
        print(")")

    def isNext(self, other):
        i = (self.unconnectedNextIndex + 1) % 3
        j = (self.unconnectedNextIndex + 2) % 3

        a = (other.unconnectedPrevIndex + 1) % 3
        b = (other.unconnectedPrevIndex + 2) % 3

        if self.indices[i] == other.indices[a] and self.indices[j] == other.indices[b]:
            return True
        if self.indices[i] == other.indices[b] and self.indices[j] == other.indices[a]:
            return True
        return False

class TripletMatchInfoArray:
    TMINFO_ARRAY_STARTSIZE = 2

    def __init__(self):
        self.next = None
        self.num = 0
        self.data = [TripletMatchInfo() for _ in range(TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE)]

    @staticmethod
    def allocSize(numEl):
        size = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE
        while size < numEl:
            size <<= 1
        return size

    def add(self, info, alloc, level):
        pos = self.num
        self.num += 1
        thisSize = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE << level
        if pos < thisSize:
            self.data[pos] = info
from typing import List

class TripletMatchInfo:
    def __init__(self):
        self.coords = [0.0] * 3
        self.indices = [0] * 3
        self.unconnectedNextIndex = 0

    def isNext(self, other: 'TripletMatchInfo') -> bool:
        return True  # Placeholder for actual implementation

    def dump(self):
        print(f"Coords: {self.coords}, Indices: {self.indices}")

class TripletMatchAllocator:
    def newTripletMatchInfoArray(self, size: int) -> 'TripletMatchInfoArray':
        return TripletMatchInfoArray(size)

class TripletMatchInfoArray:
    TMINFO_ARRAY_STARTSIZE = 16

    def __init__(self, size: int = TMINFO_ARRAY_STARTSIZE):
        self.next = None
        self.num = 0
        self.data = [TripletMatchInfo() for _ in range(size)]

    @staticmethod
    def allocSize(numEl: int) -> int:
        size = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE
        while size < numEl:
            size <<= 1
        return size

    def add(self, info: TripletMatchInfo, alloc: TripletMatchAllocator, level: int):
        pos = self.num
        self.num += 1
        thisSize = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE << level
        if pos < thisSize:
            self.data[pos] = info
        elif pos == thisSize:
            newarray = alloc.newTripletMatchInfoArray(thisSize << 1)
            newarray.data[0] = info
            newarray.num = 1
            self.next = newarray
        else:
            self.next.add(info, alloc, level + 1)

    def get(self, i: int, level: int) -> TripletMatchInfo:
        thisSize = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE << level
        if i < thisSize:
            return self.data[i]
        return self.next.get(i - thisSize, level + 1)

    def dump(self, level: int):
        print(f"{self.num}:")
        thisSize = TripletMatchInfoArray.TMINFO_ARRAY_STARTSIZE << level
        for info in self.data[:thisSize]:
            info.dump()
        if self.next:
            self.next.dump(level + 1)

class TripletMatch:
    def __init__(self, mid: int):
        self.mustMatch = 0
        self.nextMustMatch = 0
        self.currIndex = -1
        self.matches = [[] for _ in range(mid)]

    def hasMatch(self) -> bool:
        return self.currIndex >= 0

    def add(self, tminfo: TripletMatchInfo, trip: 'QueryTriplet', tripIndex: int, alloc: TripletMatchAllocator) -> bool:
        if tripIndex == self.currIndex + 1:
            self.mustMatch = self.nextMustMatch
            self.nextMustMatch = 0
            self.currIndex += 1

        if currIndex > 0:
            for distback in range(currIndex):
                prev = currIndex - 1 - distback
                puncon = trip.getPrevUnconnected()
                n = len(self.matches[prev])
                for i in range(n):
                    pmatch = self.matches[prev][i]
                    if distback > 0 or pmatch.isNext(tminfo):
                        d = pmatch.coords[pmatch.unconnectedNextIndex].distSQ(
                            tminfo.coords[puncon])
                        if trip.goodKDistance(d, distback):
                            break
                else:
                    return False

        badi = tminfo.unconnectedNextIndex
        i1 = (badi + 1) % 3
        i2 = (badi + 2) % 3

        self.nextMustMatch |= (1 << tminfo.indices[i1]) | (1 << tminfo.indices[i2])

        self.matches[tripIndex].add(tminfo, alloc)
        return True

class QueryTriplet:
    def getPrevUnconnected(self) -> int:
        return 0  # Placeholder for actual implementation

    def goodKDistance(self, d: float, distback: int) -> bool:
        return True  # Placeholder for actual implementation
class QueryTriplet:
    def getPrevUnconnected(self) -> int:
        return 0  # Placeholder for actual implementation

    def goodKDistance(self, d: float, distback: int) -> bool:
        return True  # Placeholder for actual implementation

class TripletMatchHash:
    prime_list = [13, 17, 29, 37, 53, 67, 89, 109, 139, 167, 199, 239, 281, 331, 383, 443, 509, 587, 677, 773, 881, 1009]
    endPrimeIndex = len(prime_list) - 1

    def __init__(self, alloc):
        self.prime_index = 12
        self.table_size = TripletMatchHash.prime_list[self.prime_index]
        self.num_elements = 0
        self.alloc = alloc
        self.table = [None] * self.table_size

    def grow(self):
        new_table_size = TripletMatchHash.prime_list[min(self.endPrimeIndex, self.prime_index + 1)]
        new_table = [None] * new_table_size
        for item in self.table:
            if item is not None:
                pos = self.hash(item.id) % new_table_size
                while new_table[pos] is not None:
                    pos += 1
                    if pos >= new_table_size:
                        pos = 0
                new_table[pos] = item
        self.table = new_table
        self.table_size = new_table_size
        self.prime_index += 1

    def hash(self, id: int) -> int:
        m = 0xc6a4a7935bd1e995
        r = 47
        h = 8 * m
        k = id
        k *= m
        k ^= (k >> r)
        k *= m

        h ^= k
        h *= m

        h ^= (h >> r)
        h *= m
        h ^= (h >> r)

        return h % self.table_size

    def getPos(self, id: int) -> int:
        pos = self.hash(id)
        while self.table[pos] is not None:
            if self.table[pos].id == id:
                return pos
            pos += 1
            if pos >= self.table_size:
                pos = 0
        return -1

    def exists(self, key: int) -> 'TripletMatch':
        pos = self.getPos(key)
        if pos != -1:
            return self.table[pos]
        return None

class TripletMatches:
    class HeadType:
        def __init__(self):
            self.head = 0
            self.padding = [0] * 16

    def __init__(self, alloc, params, sz, nthreads):
        self.params = params
        self.alloc = alloc
        self.seenMatches = TripletMatchHash(alloc)
        self.heads = [TripletMatches.HeadType() for _ in range(nthreads)]
        self.counts = [0] * sz
        self.curIndex = 0
        self.qsize = sz

        for i in range(nthreads):
            self.heads[i].head = i

    def nextIndex(self) -> bool:
        stillgood = self.counts[self.curIndex]
        self.curIndex += 1
        assert self.curIndex <= self.qsize, "curIndex should not exceed qsize"
        return stillgood

    def add(self, mid: int, tdata, trip: QueryTriplet, which: int) -> bool:
        key = tdata.molPos
        match = None

        if tdata.nrot < self.params.minRot or tdata.nrot > self.params.maxRot:
            return False
        if tdata.weight < self.params.reducedMinWeight or tdata.weight > self.params.reducedMaxWeight:
            return False

        if self.curIndex > 0:
            match = self.seenMatches.exists(key)
            if match is None:
                return False
            if not match.hasValidConnections(tdata, trip, self.curIndex):
                return False
            if not trip.isMatch(tdata):
                return False

        # Assuming TripletMatch class has a method to add new matches
        match = self.alloc.createTripletMatch(mid, tdata)
        pos = self.hash(key) % self.table_size
        while self.table[pos] is not None:
            pos += 1
            if pos >= self.table_size:
                pos = 0
        self.table[pos] = match
        self.num_elements += 1

        return True
class TripletMatching:
    def __init__(self, table_size):
        self.table = [None] * table_size
        self.table_size = table_size
        self.num_elements = 0

    def hash(self, key):
        return hash(key) % self.table_size

    def add(self, mid, tdata, trip, curIndex):
        if not trip.isMatch(tdata):
            return False

        match = self.alloc.createTripletMatch(mid, tdata)
        pos = self.hash(key) % self.table_size
        while self.table[pos] is not None:
            pos += 1
            if pos >= self.table_size:
                pos = 0
        self.table[pos] = match
        self.num_elements += 1

        return True

    def pop(self, t):
        nthreads = len(self.heads)
        assert t < nthreads
        while self.heads[t].head < len(self.seenMatches):
            pos = self.heads[t].head
            self.heads[t].head += nthreads

            if self.seenMatches[pos] is not None:
                match = self.seenMatches[pos]
                if match.valid():
                    return True
        return False

    def total(self):
        return self.counts[-1]

    def empty(self, t):
        return len(self.seenMatches) <= self.heads[t].head

    def dumpCnts(self):
        for count in self.counts:
            print(count, end=" ")
        print()

    def getQSize(self):
        return self.qsize

    def numChunks(self):
        return self.alloc.numChunks()