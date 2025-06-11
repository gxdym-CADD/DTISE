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
BitSetTree.py

A bitset tree. A balanced tree that organizes bitsets, in this case
triplet fingerprints. Right now this is experimental and assumes
everything can fit in memory.
Created on: Jan 4, 2011
Author: dkoes
"""

from typing import List, Tuple
import numpy as np

class TripletFingerprint:
    def __init__(self, bits: np.ndarray):
        self.bits = bits

    def getBit(self, index: int) -> bool:
        return self.bits[index]

    def bitcnt(self) -> int:
        return np.sum(self.bits)

    def __or__(self, other: 'TripletFingerprint') -> 'TripletFingerprint':
        return TripletFingerprint(np.bitwise_or(self.bits, other.bits))

    def __and__(self, other: 'TripletFingerprint') -> 'TripletFingerprint':
        return TripletFingerprint(np.bitwise_and(self.bits, other.bits))

class BitSetTree:
    class Node:
        def __init__(self, ored: TripletFingerprint = None, anded: TripletFingerprint = None,
                     left: int = 0, right: int = 0, dist: int = 0):
            self.ored = ored if ored is not None else TripletFingerprint(np.zeros(256, dtype=bool))
            self.anded = anded if anded is not None else TripletFingerprint(np.ones(256, dtype=bool))
            self.left = left
            self.right = right
            self.dist = dist

        def __init__(self, v: TripletFingerprint):
            self.ored = v
            self.anded = v
            self.left = 0
            self.right = 0
            self.dist = 0

        def __init__(self, l: int, r: int, lc: 'BitSetTree.Node', rc: 'BitSetTree.Node'):
            self.ored = lc.ored | rc.ored
            self.anded = lc.anded & rc.anded
            self.left = l
            self.right = r
            self.dist = max(lc.dist, rc.dist) + 1

    def __init__(self):
        self.tree: List[BitSetTree.Node] = []
        self.root: int = -1
        self.levels: int = 0

    def distance(self, a: TripletFingerprint, b: TripletFingerprint) -> int:
        return np.sum(a.bits != b.bits)

    def construct_tree(self, fingerprints: List[TripletFingerprint]):
        self.tree.clear()
        num_fingerprints = len(fingerprints)
        if num_fingerprints == 0:
            return

        # Initialize the tree with individual nodes
        for fp in fingerprints:
            self.tree.append(BitSetTree.Node(fp))

        while len(self.tree) > 1:
            new_tree: List[BitSetTree.Node] = []
            for i in range(0, len(self.tree), 2):
                if i + 1 < len(self.tree):
                    node = BitSetTree.Node(i, i + 1, self.tree[i], self.tree[i + 1])
                else:
                    node = self.tree[i]
                new_tree.append(node)
            self.tree = new_tree

        self.root = 0
        self.levels = int(np.log2(len(fingerprints))) if len(fingerprints) > 1 else 1

    def search(self, query: TripletFingerprint, k: int = 1) -> List[Tuple[int, float]]:
        results = []

        def traverse(node_index: int):
            if node_index < len(self.tree):
                node = self.tree[node_index]
                dist = self.distance(query, node.ored)
                if len(results) < k:
                    results.append((node_index, dist))
                    results.sort(key=lambda x: x[1])
                elif dist < results[-1][1]:
                    results.pop()
                    results.append((node_index, dist))
                    results.sort(key=lambda x: x[1])

                # Traverse the tree based on distance
                if node.left != 0 and (len(results) < k or dist <= results[-1][1]):
                    traverse(node.left)
                if node.right != 0 and (len(results) < k or dist <= results[-1][1]):
                    traverse(node.right)

        traverse(self.root)
        return [(self.tree[i[0]].ored, i[1]) for i in results]

# Example usage
if __name__ == "__main__":
    # Create some example fingerprints
    fps = [TripletFingerprint(np.random.randint(2, size=256).astype(bool)) for _ in range(10)]
    
    # Construct the bitset tree
    bst = BitSetTree()
    bst.construct_tree(fps)
    
    # Search for the nearest neighbors of a query fingerprint
    query_fp = TripletFingerprint(np.random.randint(2, size=256).astype(bool))
    nearest_neighbors = bst.search(query_fp, k=3)
    
    print("Nearest Neighbors:")
    for nn in nearest_neighbors:
        print(f"Fingerprint: {nn[0].bits}, Distance: {nn[1]}")
import numpy as np
from collections import deque

class TripletFingerprint:
    def __init__(self, bits):
        self.bits = bits

    def getBit(self, pos):
        return self.bits[pos]

class BitSetTree:
    class Node:
        def __init__(self):
            self.anded = np.zeros(256, dtype=bool)
            self.ored = np.zeros(256, dtype=bool)
            self.left = 0
            self.right = 0

    def __init__(self):
        self.tree = [BitSetTree.Node()]
        self.levels = 0
        self.root = 0

    def construct_tree(self, fps):
        self.construectPeelTD(fps)

    def search(self, query_fp, k):
        # Placeholder for the search logic
        return []

    def construectPeelTD(self, fingers):
        tree.reserve(len(fingers) * 2 + 1)
        tree.resize(1)  # blank node at index zero
        levels = 0
        root = self.createPeelNode(fingers, 1)

    def createPeelNode(self, fingers, l):
        if len(fingers) == 0:
            return 0

        if l > self.levels:
            self.levels = l
        ret = len(self.tree)
        self.tree.append(BitSetTree.Node())

        self.tree[ret].anded[:] = True
        for i in range(len(fingers)):
            self.tree[ret].anded &= fingers[i].bits
            self.tree[ret].ored |= fingers[i].bits

        if l == 10:
            print("LevelSize", l, np.sum(self.tree[ret].ored))

        if np.all(self.tree[ret].anded == self.tree[ret].ored):
            return ret
        else:
            left_fingers = []
            right_fingers = []
            for f in fingers:
                if self.tree[ret].anded & f.bits:
                    left_fingers.append(f)
                else:
                    right_fingers.append(f)

            self.tree[ret].left = self.createPeelNode(left_fingers, l + 1)
            self.tree[ret].right = self.createPeelNode(right_fingers, l + 1)
            return ret

    def split(self, fingers):
        if len(fingers) <= 1:
            return fingers, []

        max_bit_count = 0
        best_pos = -1
        for pos in range(256):
            bit_count = np.sum([f.getBit(pos) for f in fingers])
            if bit_count > max_bit_count:
                max_bit_count = bit_count
                best_pos = pos

        left_fingers = [f for f in fingers if f.getBit(best_pos)]
        right_fingers = [f for f in fingers if not f.getBit(best_pos)]
        return left_fingers, right_fingers

# Example usage
fps = [TripletFingerprint(np.random.randint(2, size=256)) for _ in range(10)]
bitset_tree = BitSetTree()
bitset_tree.construct_tree(fps)
import numpy as np

class TripletFingerprint:
    def __init__(self, bits):
        self.bits = bits

    def getBit(self, pos):
        return self.bits[pos]

    def contains(self, other):
        return all(a or not b for a, b in zip(self.bits, other.bits))

    def setAll(self):
        self.bits = np.ones_like(self.bits)

    def __and__(self, other):
        return TripletFingerprint(np.bitwise_and(self.bits, other.bits))

    def __or__(self, other):
        return TripletFingerprint(np.bitwise_or(self.bits, other.bits))

    def bitcnt(self):
        return np.sum(self.bits)

class BitSetTree:
    class Node:
        def __init__(self):
            self.anded = TripletFingerprint(np.zeros(256))
            self.ored = TripletFingerprint(np.zeros(256))
            self.left = 0
            self.right = 0
            self.dist = 0

    def __init__(self):
        self.tree = [BitSetTree.Node()]
        self.levels = 0
        self.root = 0
        self.nonzeroRoots = []
        self.fingerHeap = []
        self.heapSkip = 16

    def splitpca(self, fingers, left, right):
        t_count = np.sum([f.getBit(pos) for f in fingers])
        if t_count > max_bit_count:
            max_bit_count = t_count
            best_pos = pos

        left_fingers = [f for f in fingers if f.getBit(best_pos)]
        right_fingers = [f for f in fingers if not f.getBit(best_pos)]

    def createMiniHeap(self, n, heap, pos, max):
        if pos >= max:
            assert n == 0
            return

        if n == 0:
            heap[pos].setAll()
            self.createMiniHeap(0, heap, 2 * pos, max)
            self.createMiniHeap(0, heap, 2 * pos + 1, max)
        else:
            heap[pos] = self.tree[n].anded
            self.createMiniHeap(self.tree[n].left, heap, 2 * pos, max)
            self.createMiniHeap(self.tree[n].right, heap, 2 * pos + 1, max)

    def createFingerHeap_r(self, n, depth):
        if n == 0:
            return
        if self.tree[n].dist > depth:
            self.createFingerHeap_r(self.tree[n].left, depth)
            self.createFingerHeap_r(self.tree[n].right, depth)
        elif self.tree[n].dist == depth:
            miniheap = [TripletFingerprint(np.zeros(256)) for _ in range(self.heapSkip)]
            self.createMiniHeap(n, miniheap, 1, self.heapSkip)
            self.fingerHeap.extend(miniheap)
        else:
            raise Exception("Invalid state")

    def computeDists(self, n):
        if n == 0:
            return
        if self.tree[n].left == 0 and self.tree[n].right == 0:
            self.tree[n].dist = 0
        elif self.tree[n].left == 0:
            self.computeDists(self.tree[n].right)
            self.tree[n].dist = self.tree[self.tree[n].right].dist + 1
        elif self.tree[n].right == 0:
            self.computeDists(self.tree[n].left)
            self.tree[n].dist = self.tree[self.tree[n].left].dist + 1
        else:
            self.computeDists(self.tree[n].left)
            self.computeDists(self.tree[n].right)
            self.tree[n].dist = max(self.tree[self.tree[n].left].dist, self.tree[self.tree[n].right].dist) + 1

    def containedInMiniHeap(self, start, off, bset):
        if off >= self.heapSkip:
            return True
        if bset.contains(self.fingerHeap[start + off]):
            if self.containedInMiniHeap(start, 2 * off, bset):
                return True
            if self.containedInMiniHeap(start, 2 * off + 1, bset):
                return True
        return False

    def construct(self, alg=ConstructAlg.PCASplit):
        # Implement the construction algorithm based on the enum value
        pass

class ConstructAlg:
    GreedyBottomUp = "GreedyBottomUp"
    PeelTopDown = "PeelTopDown"
    PCASplit = "PCASplit"
from typing import List, Tuple

class BitSetTree:
    class ConstructAlg:
        GreedyBottomUp = "GreedyBottomUp"
        PeelTopDown = "PeelTopDown"
        PCASplit = "PCASplit"

    def __init__(self):
        self.root = 0
        self.levels = 0
        self.heapSkip = 0
        self.tree = []
        self.fingerHeap = []
        self.nonzeroRoots = []

    def containedInMiniHeap(self, start: int, off: int, bset) -> bool:
        # Implement the logic for checking containment in a mini heap
        pass

    def constructGreedyBU(self, fingers):
        # Implement the greedy bottom-up construction algorithm
        pass

    def construectPeelTD(self, fingers):
        # Implement the peel top-down construction algorithm
        pass

    def constructPCA(self, fingers):
        # Implement the PCA split construction algorithm
        pass

    def computeDists(self, node: int):
        # Implement the logic to compute distances
        pass

    def addNonZeroRoots(self, node: int):
        # Implement the logic to add non-zero roots
        pass

    def createFingerHeap_r(self, node: int, depth: int):
        # Implement the recursive finger heap creation
        pass

    def construct(self, fingers: List[Tuple[int, int, int]], alg=ConstructAlg.PCASplit):
        self.tree.clear()
        self.root = 0
        self.levels = 0
        if alg == self.ConstructAlg.GreedyBottomUp:
            self.constructGreedyBU(fingers)
        elif alg == self.ConstructAlg.PeelTopDown:
            self.construectPeelTD(fingers)
        elif alg == self.ConstructAlg.PCASplit:
            self.constructPCA(fingers)

        self.computeDists(self.root)
        self.addNonZeroRoots(self.root)
        if len(self.nonzeroRoots) > 0:
            d = self.tree[self.nonzeroRoots[0]].dist
            self.heapSkip = 1 << (d + 1)
            self.createFingerHeap_r(self.root, d)

    def printInfo(self):
        if self.root == 0:
            return

        identical_cnt = 0
        leaf_cnt = 0
        for i in range(1, len(self.tree)):
            if self.tree[i].left == 0 and self.tree[i].right == 0:
                leaf_cnt += 1
            if self.tree[i].left != 0 and self.tree[i].anded == self.tree[i].ored:
                identical_cnt += 1

        print(f"Leaves: {leaf_cnt}")
        print(f"Identical: {identical_cnt}")

        levelbitcnts = []

        def computeBitCnts(levelbitcnts, node, depth):
            # Implement the logic to compute bit counts
            pass

        computeBitCnts(levelbitcnts, self.tree[self.root], 0)

        for vec in levelbitcnts:
            print(" ".join(map(str, vec)))

    def hasContainedIn(self, bset) -> bool:
        for i in range(0, len(self.fingerHeap), self.heapSkip):
            if self.containedInMiniHeap(i, 1, bset):
                return True
        return False

# Assuming TripletFingerprint is a class or struct defined elsewhere
class TripletFingerprint:
    def contains(self, fingerprint) -> bool:
        # Implement the logic to check containment
        pass