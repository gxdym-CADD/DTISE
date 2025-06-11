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
DataViewers.h

Created on: Oct 18, 2011
Author: dkoes

Some interfaces for looking at tree data the generalize leaf (single tree)
and node (double tree) data.
"""

from typing import List, Optional
import copy

# a slice of a dataviewer, the trees are always allocated (not mapped to data)
class Cluster:
    def __init__(self):
        self.indices: List[int] = []
        self.MIV: Optional['MappableOctTree'] = None
        self.MSV: Optional['MappableOctTree'] = None

    @classmethod
    def from_cluster(cls, rhs: 'Cluster') -> 'Cluster':
        new_instance = cls()
        new_instance.indices = copy.deepcopy(rhs.indices)
        if rhs.MIV:
            new_instance.MIV = rhs.MIV.clone()
        if rhs.MSV:
            new_instance.MSV = rhs.MSV.clone()
        return new_instance

    @classmethod
    def from_data(cls, inds: List[int], mivs: List['MappableOctTree'], msvs: List['MappableOctTree']) -> 'Cluster':
        instance = cls()
        instance.indices = inds
        instance.MIV = MappableOctTree.create_from_intersection(len(inds), mivs)
        instance.MSV = MappableOctTree.create_from_union(len(inds), msvs)
        return instance

    def set_to_singleton(self, i: int, miv: 'MappableOctTree', msv: 'MappableOctTree'):
        self.clear()
        self.indices.append(i)
        self.MIV = miv.clone()
        self.MSV = msv.clone()

    def is_valid(self) -> bool:
        return self.MIV is not None and self.MSV is not None

    def size(self) -> int:
        return len(self.indices)

    def __getitem__(self, i: int) -> int:
        return self.indices[i]

    # invalidates a and b
    def merge_into(self, a: 'Cluster', b: 'Cluster'):
        self.indices.extend(a.indices)
        self.indices.extend(b.indices)

        itrees = [a.MIV, b.MIV]
        self.MIV = MappableOctTree.create_from_intersection(2, itrees)

        utrees = [a.MSV, b.MSV]
        self.MSV = MappableOctTree.create_from_union(2, utrees)

        a.clear()
        b.clear()

    # invalidates a
    def add_into(self, a: 'Cluster'):
        self.indices.extend(a.indices)
        itrees = [self.MIV, a.MIV]
        self.MIV = MappableOctTree.create_from_intersection(2, itrees)

        utrees = [self.MSV, a.MSV]
        self.MSV = MappableOctTree.create_from_union(2, utrees)

        a.clear()

    # invalidates a
    def move_into(self, a: 'Cluster'):
        self.indices, a.indices = a.indices, self.indices
        self.MIV, a.MIV = a.MIV, None
        self.MSV, a.MSV = a.MSV, None

        a.clear()

    def clear(self):
        if self.MIV:
            self.MIV.free()
            self.MIV = None
        if self.MSV:
            self.MSV.free()
            self.MSV = None
        self.indices.clear()

# a wrapper that can view single tree leaves the same as internal nodes
class DataViewer:
    def __init__(self):
        self.treeptr: bytes = b""
class DataView:
    def __init__(self):
        self.indices = []
        self.MIV = None
        self.MSV = None

    def swap(self, a: 'DataView'):
        self.indices, a.indices = a.indices, self.indices
        self.MIV, a.MIV = a.MIV, None
        self.MSV, a.MSV = a.MSV, None

        a.clear()

    def clear(self):
        if self.MIV:
            self.MIV.free()
            self.MIV = None
        if self.MSV:
            self.MSV.free()
            self.MSV = None
        self.indices.clear()

# A wrapper that can view single tree leaves the same as internal nodes
class DataViewer:
    def __init__(self):
        self.treeptr: bytes = b""

    # Create a reindexed subview
    def __init_subclass__(cls, par, indices):
        super().__init__()
        cls.treeptr = par.treeptr
        cls.pointtos = [par.pointtos[i] for i in indices]
        cls.treeindices = [par.treeindices[i] for i in indices]

    # Constructor
    def __init__(self, data, treei, pt):
        self.treeptr = data
        self.pointtos, pt = pt, self.pointtos
        self.treeindices, treei = treei, self.treeindices
        assert len(self.pointtos) == len(self.treeindices)
        pt.reserve(len(self.pointtos) // 2)
        treei.reserve(len(self.treeindices) // 2)

    def __del__(self):
        pass

    # These are file indices
    def getMSV(self, i: int) -> 'MappableOctTree':
        raise NotImplementedError

    def getMIV(self, i: int) -> 'MappableOctTree':
        raise NotImplementedError

    def getIndex(self, i: int) -> int:
        return self.pointtos[i]

    def size(self) -> int:
        return len(self.treeindices)

    def isLeaf(self) -> bool:
        raise NotImplementedError

    def createSlice(self, indices: list[int]) -> 'DataViewer':
        raise NotImplementedError

# This class has pointers to single trees and the actual object data
class LeafViewer(DataViewer):
    def __init__(self, par, indices):
        super().__init_subclass__(par, indices)

    def __init__(self, data, treei, pt):
        super().__init__(data, treei, pt)

    def getMSV(self, i: int) -> 'MappableOctTree':
        return MappableOctTree.from_buffer_copy(self.treeptr[self.treeindices[i]:])

    def getMIV(self, i: int) -> 'MappableOctTree':
        return MappableOctTree.from_buffer_copy(self.treeptr[self.treeindices[i]:])

    def isLeaf(self) -> bool:
        return True

    def createSlice(self, indices: list[int]) -> 'DataViewer':
        return LeafViewer(self, indices)

# This class has pointers to double trees and nodes
class NodeViewer(DataViewer):
    def __init__(self, par, indices):
        super().__init_subclass__(par, indices)

    def __init__(self, data, treei, pt):
        super().__init__(data, treei, pt)

    def getMSV(self, i: int) -> 'MappableOctTree':
        dbl = GSSDoubleTree.from_buffer_copy(self.treeptr[self.treeindices[i]:])
        return dbl.getMSV()

    def getMIV(self, i: int) -> 'MappableOctTree':
        dbl = GSSDoubleTree.from_buffer_copy(self.treeptr[self.treeindices[i]:])
        return dbl.getMIV()

    def isLeaf(self) -> bool:
        return False

    def createSlice(self, indices: list[int]) -> 'DataViewer':
        return NodeViewer(self, indices)