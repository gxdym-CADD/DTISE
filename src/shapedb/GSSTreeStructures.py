# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

import struct

class MappableOctTree:
    def bytes(self):
        pass

    def write(self, out):
        pass

class GSSTypes:
    pass

class GSSDoubleTree:
    def __init__(self, msv_offset, data):
        self.msvOffset = msv_offset
        self.data = data

    @staticmethod
    def writeTreeS(out, miv, msv):
        p = miv.bytes()
        out.write(struct.pack('I', p))
        miv.write(out)
        msv.write(out)

    def getMIV(self):
        return MappableOctTree.from_bytes(self.data)

    def getMSV(self):
        return MappableOctTree.from_bytes(self.data[self.msvOffset:])

class GSSNodeCommon:
    def __init__(self, is_leaf, N):
        self.isLeaf = is_leaf
        self.N = N

class GSSLeaf:
    class Child:
        def __init__(self, object_pos, tree):
            self.object_pos = object_pos
            self.tree = tree

    def __init__(self, info, child_positions):
        self.info = info
        self.child_positions = child_positions

    @staticmethod
    def writeLeaf(data, cluster, outNodes, outTrees):
        pass

    def getChild(self, i):
        d = data()
        return struct.unpack_from('Q', d, self.child_positions[i])[0]

    def data(self):
        return struct.pack('I' * len(self.child_positions), *self.child_positions)

    def size(self):
        return self.info.N

    def bytes(self):
        pass

class GSSInternalNode:
    class Child:
        def __init__(self, isLeaf=False, node_pos=0, leaves_start=0, leaves_end=0, MSVindex=0, data=b''):
            self.isLeaf = isLeaf
            self.node_pos = node_pos
            self.leaves_start = leaves_start
            self.leaves_end = leaves_end
            self.MSVindex = MSVindex
            self.data = data

        def getMIV(self):
            return MappableOctTree.from_bytes(self.data)

        def getMSV(self):
            return MappableOctTree.from_bytes(self.data[self.MSVindex:])

        def position(self):
            return self.node_pos

        def isLeafPosition(self):
            return self.isLeaf

        def bytes(self):
            pass

    def __init__(self, info, child_positions):
        self.info = info
        self.child_positions = child_positions

    @staticmethod
    def writeNode(data, cluster, outNodes, outTrees):
        pass

    @staticmethod
    def createMergedNode(nodes):
        pass

    def getChild(self, i):
        d = data()
        return struct.unpack_from('Q', d, self.child_positions[i])[0]

    def size(self):
        return self.info.N

    def bytes(self):
        pass

    def data(self):
        return struct.pack('I' * len(self.child_positions), *self.child_positions)

    def createTruncated(self, dimension, resolution):
        pass

    def setChildPos(self, i, newpos, isLeaf, lstart, lend):
        pass