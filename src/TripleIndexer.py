import numpy as np
from collections import defaultdict

class TripleIndexer:
    def __init__(self, n=None):
        self.reverse = []
        self.lookup = None
        self.sz = 0
        self.pharmasz = 0
        if n is not None:
            self.set(n)

    def set(self, n):
        if self.pharmasz == n:
            return
        self.pharmasz = n

        # Create a 3D numpy array for fast lookup
        self.lookup = np.zeros((n, n, n), dtype=int)
        
        from scipy.special import comb
        cnt = int(comb(n + 2, 3))
        self.reverse = [None] * cnt

        counter = defaultdict(int)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    ijk = sorted([i, j, k])
                    index = counter[tuple(ijk)]
                    if index > 0:
                        self.lookup[i][j][k] = index
                    else:
                        index = len(counter) + 1
                        self.lookup[i][j][k] = index
                        counter[tuple(ijk)] = index
                        assert index <= cnt
                        self.reverse[index - 1] = tuple(ijk)

        assert cnt == len(counter)
        self.sz = cnt

    def __call__(self, i, j, k):
        return self.lookup[i][j][k]

    def getIJK(self, pos, i=None, j=None, k=None):
        assert pos < len(self.reverse)
        if i is not None:
            i[0] = self.reverse[pos][0]
        if j is not None:
            j[0] = self.reverse[pos][1]
        if k is not None:
            k[0] = self.reverse[pos][2]

    def size(self):
        return self.sz

    def dump(self, out):
        for p in range(len(self.reverse)):
            i, j, k = self.reverse[p]
            out.write(f"{i} {j} {k} {p}\n")