class Vertex:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, rhs):
        if self.x != rhs.x:
            return self.x < rhs.x
        if self.y != rhs.y:
            return self.y < rhs.y
        return self.z < rhs.z

    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z

    def distance_sq(self, rhs):
        X = self.x - rhs.x
        Y = self.y - rhs.y
        Z = self.z - rhs.z

        return X * X + Y * Y + Z * Z

MINDEX_BITS = 15

class MOctNode:
    def __init__(self, vol=0.0):
        self.vol = vol
        self.children = [MChildNode() for _ in range(8)]

class MChildNode:
    def __init__(self, is_leaf=True, index=0, pattern=0, numbits=0):
        self.is_leaf = is_leaf
        if is_leaf:
            self.leaf_pattern = pattern
            self.leaf_numbits = numbits
        else:
            self.node_index = index

    def intersect_union_volume(self, tree, rhs, rtree, cube_vol, intersectval, unionval):
        # Implementation of intersectUnionVolume
        pass

    def intersect_volume(self, tree, rhs, rtree):
        # Implementation of intersectVolume
        pass

    def union_volume(self, tree, rhs, rtree):
        # Implementation of unionVolume
        pass

    def invert(self, tree, maxvol):
        # Implementation of invert
        pass

    def contained_in(self, tree, rhs, rtree):
        # Implementation of containedIn
        pass

    def volume(self, tree, dim3):
        # Implementation of volume
        pass

    def equals(self, tree, rhs, rtree):
        # Implementation of equals
        pass

    def collect_vertices(self, vertices, box, tree):
        # Implementation of collectVertices
        pass

    def check_coord(self, tree, i, j, k, max_val):
        # Implementation of checkCoord
        pass

    def count_leaves_at_depths(self, tree, depth, counts):
        # Implementation of countLeavesAtDepths
        pass

class MappableOctTree:
    def __init__(self, dim, r, nodes):
        self.root = r
        self.dimension = dim
        self.N = len(nodes)
        self.tree = [MOctNode(vol=node.vol) for node in nodes]

    @staticmethod
    def create_from_r(N, nodes, trees, newtree, is_union, cube_vol):
        # Implementation of createFrom_r
        pass

    def create_truncated_r(self, node, res, fill_in, newtree, cube_vol):
        # Implementation of createTruncated_r
        pass
class MOctNode:
    def __init__(self, vol=0):
        self.vol = vol
        self.children = [None] * 8

class MChildNode:
    def __init__(self, is_leaf=False, leaf=None, node=None):
        self.isLeaf = is_leaf
        if leaf is None:
            leaf = {'pattern': 0, 'numbits': 0}
        self.leaf = leaf
        if node is None:
            node = {'index': 0}
        self.node = node

class MappableOctTree:
    def __init__(self, dim, r, nodes):
        self.root = r
        self.dimension = dim
        self.N = len(nodes)
        self.tree = [MOctNode(vol=node.vol) for node in nodes]

    @staticmethod
    def create_from_r(N, nodes, trees, newtree, is_union, cube_vol):
        # Implementation of createFrom_r
        pass

    def create_truncated_r(self, node, res, fill_in, newtree, cube_vol):
        # Implementation of createTruncated_r
        pass

    def __init__(self, rhs):
        self.root = rhs.root
        self.dimension = rhs.dimension
        self.N = rhs.N
        self.tree = [MOctNode(vol=node.vol) for node in rhs.tree]

    @staticmethod
    def create_from_intersection(N, in_trees):
        # Implementation of createFromIntersection
        pass

    @staticmethod
    def create_from_union(N, in_trees):
        # Implementation of createFromUnion
        pass

    def clone(self):
        return MappableOctTree(self)

    def invert(self):
        # Implementation of invert
        pass

    def create_truncated(self, res, fill_in):
        # Implementation of createTruncated
        pass

    def create_rounded(self, vol, fill_in):
        # Implementation of createRounded
        pass

    @staticmethod
    def create_rounded_set(N, in_trees, round_up, out_trees):
        # Implementation of createRoundedSet
        pass

    def intersect_volume(self, rhs):
        # Implementation of intersectVolume
        pass

    def union_volume(self, rhs):
        # Implementation of unionVolume
        pass

    def intersect_union_volume(self, rhs, ival, uval):
        # Implementation of intersectUnionVolume
        pass

    def contained_in(self, rhs):
        # Implementation of containedIn
        pass

    def volume(self):
        # Implementation of volume
        pass

    def leaves(self):
        # Implementation of leaves
        pass

    def write(self, out):
        # Implementation of write
        pass

    @staticmethod
    def create_r(res, cube, obj, tree):
        if cube.get_size() <= res:  # must be a leaf
            ret = MChildNode(is_leaf=True)
            x, y, z = cube.get_center()
            if obj.contains_point(x, y, z):
                ret.leaf['pattern'] = 0xff
                ret.leaf['numbits'] = 8
            else:
                ret.leaf['pattern'] = 0
                ret.leaf['numbits'] = 0
            return ret

        # does the object overlap with this cube?
        intersects = obj.intersects(cube)
        if not intersects:
            # no overlap, all done
            ret = MChildNode(is_leaf=True)
            ret.leaf['pattern'] = 0
            ret.leaf['numbits'] = 0
            return ret

        # subdivide into children
        ret = MChildNode(is_leaf=False)
        filledcnt = 0
        pat = 0
        bitcnt = 0
        pos = len(tree)
        ret.node['index'] = pos

        if len(tree) >= (1 << MINDEX_BITS):
            print("Too many nodes for MINDEX_BITS. Must recompile to support larger octrees.")
            exit(1)

        tree.append(MOctNode())
        tree[pos].vol = 0
        for i in range(8):
            newc = cube.get_octant(i)
            child = MappableOctTree.create_r(res, newc, obj, tree)
            tree[pos].children[i] = child
            if child.isLeaf:
                if child.leaf['pattern'] == 0:
                    filledcnt += 1
                elif child.leaf['pattern'] == 0xff:
                    filledcnt += 1
from typing import List, Any, Optional
import sys

class Cube:
    def __init__(self, dim: float, x: float, y: float, z: float):
        self.dim = dim
        self.x = x
        self.y = y
        self.z = z

    def get_octant(self, i: int) -> 'Cube':
        # Implement the logic to get the octant based on index i
        pass

class MGrid:
    def get_dimension(self) -> float:
        pass

    def get_resolution(self) -> float:
        pass

class MOctNode:
    def __init__(self):
        self.vol = 0
        self.children = [None] * 8

class MChildNode:
    def __init__(self, isLeaf: bool, leaf: Optional[dict] = None, volume: int = 0):
        self.isLeaf = isLeaf
        self.leaf = leaf
        self.volume = volume

class MappableOctTree:
    def __init__(self, dim: float, root: MChildNode, nodes: List[MOctNode]):
        self.dim = dim
        self.root = root
        self.nodes = nodes

    @staticmethod
    def create_r(res: float, cube: Cube, obj: Any, tree: List[MOctNode]) -> MChildNode:
        ret = MChildNode(False)
        pos = len(tree)
        if pos >= 1024:
            print("Error: Maximum depth of the octree reached. Must recompile to support larger octrees.")
            sys.exit(1)

        tree.append(MOctNode())
        tree[pos].vol = 0
        filledcnt = 0
        pat = 0
        bitcnt = 0

        for i in range(8):
            newc = cube.get_octant(i)
            child = MappableOctTree.create_r(res, newc, obj, tree)
            tree[pos].children[i] = child
            if child.isLeaf:
                if child.leaf['pattern'] == 0:
                    filledcnt += 1
                elif child.leaf['pattern'] == 0xff:
                    filledcnt += 1
                    pat |= (1 << i)
                    bitcnt += 1

            tree[pos].vol += child.volume(tree, newc.dim ** 3)

        if filledcnt == 8:
            tree.pop()
            ret.isLeaf = True
            ret.leaf = {'pattern': pat, 'numbits': bitcnt}

        return ret

    @staticmethod
    def create(dim: float, res: float, obj: Any) -> 'MappableOctTree':
        nodes = []
        root = MappableOctTree.create_r(res, Cube(dim, -dim / 2, -dim / 2, -dim / 2), obj, nodes)
        N = len(nodes)
        mem = bytearray(sizeof(MappableOctTree) + N * sizeof(MOctNode))

        ret = MappableOctTree(dim, root, nodes)

        return ret

    @staticmethod
    def create_from_grid(grid: MGrid) -> 'MappableOctTree':
        return MappableOctTree.create(grid.get_dimension(), grid.get_resolution(), grid)