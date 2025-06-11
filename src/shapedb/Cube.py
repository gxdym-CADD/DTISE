class Cube:
    def __init__(self, d, X=0, Y=0, Z=0):
        self.x = X
        self.y = Y
        self.z = Z
        self.dim = d

    def squared(self, v):
        return v * v

    def min1dist(self, a1, a2, b1, b2):
        # Try all combinations
        return min(min(abs(a1 - b2), abs(a1 - b1)), min(abs(a2 - b2), abs(a2 - b1)))

    def get_dimension(self):
        return self.dim

    def volume(self):
        return self.dim * self.dim * self.dim

    def get_center(self):
        cx = self.x + self.dim / 2
        cy = self.y + self.dim / 2
        cz = self.z + self.dim / 2
        return cx, cy, cz

    def get_bottom_corner(self):
        bx = self.x
        by = self.y
        bz = self.z
        return bx, by, bz

    def get_octant(self, i):
        res = Cube(self.dim, self.x, self.y, self.z)
        res.dim /= 2.0

        match i:
            case 0:
                pass
            case 1:
                res.x += res.dim
            case 2:
                res.y += res.dim
            case 3:
                res.x += res.dim
                res.y += res.dim
            case 4:
                res.z += res.dim
            case 5:
                res.x += res.dim
                res.z += res.dim
            case 6:
                res.y += res.dim
                res.z += res.dim
            case 7:
                res.x += res.dim
                res.y += res.dim
                res.z += res.dim
            case _:
                raise ValueError("Invalid octant index")

        return res

    def min_dist(self, rhs):
        minx = self.min1dist(self.x, self.x + self.dim, rhs.x, rhs.x + rhs.dim)
        miny = self.min1dist(self.y, self.y + self.dim, rhs.y, rhs.y + rhs.dim)
        minz = self.min1dist(self.z, self.z + self.dim, rhs.z, rhs.z + rhs.dim)

        return (minx * minx + miny * miny + minz * minz) ** 0.5