class FloatCoord:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, list) or isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        else:
            self.x = x
            self.y = y
            self.z = z

    def __iadd__(self, rhs):
        self.x += rhs.x
        self.y += rhs.y
        self.z += rhs.z
        return self

    def __isub__(self, rhs):
        self.x -= rhs.x
        self.y -= rhs.y
        self.z -= rhs.z
        return self

    def __itruediv__(self, r):
        self.x /= r
        self.y /= r
        self.z /= r
        return self

    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z

    def sqrDist(self, rhs):
        d1 = self.x - rhs.x
        d2 = self.y - rhs.y
        d3 = self.z - rhs.z
        return d1 * d1 + d2 * d2 + d3 * d3