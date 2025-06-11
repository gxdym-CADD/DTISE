class SplitType:
    NoSplit = 0
    SplitXFixed = 1
    SplitYFixed = 2
    SplitZFixed = 3

TripleInt = tuple[int, int, int]

class BoundingBox:
    def __init__(self):
        self.minx = 65535  # USHRT_MAX
        self.maxx = 0
        self.miny = 65535
        self.maxy = 0
        self.minz = 65535
        self.maxz = 0

    def update(self, ijk: TripleInt):
        self.update(ijk[0], ijk[1], ijk[2])

    def update(self, x: int, y: int, z: int):
        if x < self.minx:
            self.minx = x
        if x > self.maxx:
            self.maxx = x
        if y < self.miny:
            self.miny = y
        if y > self.maxy:
            self.maxy = y
        if z < self.minz:
            self.minz = z
        if z > self.maxz:
            self.maxz = z

    def volume(self) -> float:
        return (self.maxx - self.minx) * (self.maxy - self.miny) * (self.maxz - self.minz)

    def setX(self, min: int, max: int):
        self.minx = min
        self.maxx = max

    def setY(self, min: int, max: int):
        self.miny = min
        self.maxy = max

    def setZ(self, min: int, max: int):
        self.minz = min
        self.maxz = max

    @staticmethod
    def hasOverlap(min1: float, max1: float, min2: float, max2: float) -> bool:
        if (min1 <= max2 and min1 >= min2) or \
           (max1 <= max2 and max1 >= min2) or \
           (min2 <= max1 and min2 >= min1):
            return True
        return False

    def hasOverlap(self, x: 'BoundingBox') -> bool:
        if self.hasOverlap(self.minx, self.maxx, x.minx, x.maxx) and \
           self.hasOverlap(self.miny, self.maxy, x.miny, x.maxy) and \
           self.hasOverlap(self.minz, self.maxz, x.minz, x.maxz):
            return True
        return False

    def containedIn(self, x: 'BoundingBox') -> bool:
        if self.minx < x.minx or self.maxx > x.maxx or \
           self.miny < x.miny or self.maxy > x.maxy or \
           self.minz < x.minz or self.maxz > x.maxz:
            return False
        return True

    def planeInBox(self, split: SplitType, splitVal: int) -> bool:
        match split:
            case SplitType.SplitXFixed:
                return splitVal > self.minx and splitVal < self.maxx
            case SplitType.SplitYFixed:
                return splitVal > self.miny and splitVal < self.maxy
            case SplitType.SplitZFixed:
                return splitVal > self.minz and splitVal < self.maxz
            case _:
                raise ValueError("Invalid split type")

    def narrow(self, split: SplitType, min: int, max: int):
        match split:
            case SplitType.SplitXFixed:
                self.minx = min
                self.maxx = max
            case SplitType.SplitYFixed:
                self.miny = min
                self.maxy = max
            case SplitType.SplitZFixed:
                self.minz = min
                self.maxz = max

    def __str__(self) -> str:
        return f"BoundingBox(minx={self.minx}, maxx={self.maxx}, miny={self.miny}, maxy={self.maxy}, minz={self.minz}, maxz={self.maxz})"