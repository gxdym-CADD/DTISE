import os
import struct
from typing import List, Tuple

class MiraHeader:
    def __init__(self):
        self.fileid = bytearray(5)  # must be VOXEL
        self.control_z: int = 0  # must be 26 (0x1a)
        self.version: int = 0  # must be 1 (?)
        self.xres: int = 0
        self.yres: int = 0
        self.zres: int = 0
        self.flag: int = 0  # 0x4 if RGB data, 0x8 if RGBA data, 0 = byte data
        self.map_offset: int = 0  # must be 256
        self.voxel_offset: int = 0  # equal to 256 + (xres + yres + zres) * sizeof(double)
        self.unused = bytearray(104)  # we put resolution = num here
        self.text = bytearray(128)  # information text

class MiraObject:
    def __init__(self):
        self.header = MiraHeader()
        self.data: List[List[List[bool]]] = []
        self.maxdim: int = 0  # require cube
        self.resolution: float = 1.0  # mira objects are resolution-less, so may to set manually
                                       # our mira objects have the resolution in the unused field

    def set_resolution(self, r: float) -> None:
        self.resolution = r

    def get_resolution(self) -> float:
        return self.resolution

    def get_dimension(self) -> int:
        return self.maxdim

    def num_set_bits(self) -> int:
        cnt = 0
        for i in range(self.maxdim):
            for j in range(self.maxdim):
                for k in range(self.maxdim):
                    cnt += self.data[i][j][k]
        return cnt

    def intersects(self, cube: 'Cube') -> bool:
        return True

    def contains_point(self, x: float, y: float, z: float) -> bool:
        x /= self.resolution
        y /= self.resolution
        z /= self.resolution
        X = round(-0.5 + x + self.maxdim / 2.0)
        Y = round(-0.5 + y + self.maxdim / 2.0)
        Z = round(-0.5 + z + self.maxdim / 2.0)

        if X >= self.maxdim or Y >= self.maxdim or Z >= self.maxdim:
            return False

        return self.data[X][Y][Z]

    def write(self, out) -> None:
        out.write(self.header.text.rstrip(b'\x00'))

    def read(self, in_stream, fname: str = "") -> bool:
        header_data = in_stream.read(264)
        if len(header_data) != 264:
            return False

        self.header.fileid[:] = header_data[:5]
        self.header.control_z, self.header.version, self.header.xres, self.header.yres, \
        self.header.zres, self.header.flag, self.header.map_offset, self.header.voxel_offset = \
            struct.unpack('>BHBHHBBII', header_data[5:264])

        if self.header.fileid[0] != ord('V'):
            return False
        if self.header.flag != 0:
            print("Error: only support byte data MIRA format.")
            return False

        maxx = struct.unpack('>H', struct.pack('<H', self.header.xres))[0]
        maxy = struct.unpack('>H', struct.pack('<H', self.header.yres))[0]
        maxz = struct.unpack('>H', struct.pack('<H', self.header.zres))[0]

        if maxx != maxy or maxy != maxz:
            print("Error: only support cubic volumes.")
            return False

        self.maxdim = maxx
        self.header.text[127] = 0  # ensure null termination
        if fname:
            self.header.text[:len(fname)] = fname.encode('utf-8')

        resprefix = b"resolution = "
        prefixn = len(resprefix)
        if self.header.unused[:prefixn] == resprefix:
            resolution_str = self.header.unused[prefixn:].split(b'\x00')[0].decode('utf-8')
            self.resolution = float(resolution_str)

        # absorb map
        voxeloff = self.header.voxel_offset
        mapoff = self.header.map_offset
        while voxeloff > mapoff:
            in_stream.read(1)
            voxeloff -= 1

        return True
import os

class MiraObject:
    def __init__(self):
        self.header = None
        self.resolution = None

    def read(self, in_stream, filename):
        resprefix = b"resolution = "
        prefixn = len(resprefix)
        if self.header.unused[:prefixn] == resprefix:
            resolution_str = self.header.unused[prefixn:].split(b'\x00')[0].decode('utf-8')
            self.resolution = float(resolution_str)

        # absorb map
        voxeloff = self.header.voxel_offset
        mapoff = self.header.map_offset
        while voxeloff > mapoff:
            in_stream.read(1)
            voxeloff -= 1

        return True

class MiraIterator:
    def __init__(self, dname):
        self.files = []
        self.file_pos = 0
        self.current = MiraObject()

        # get all the mira files from the directory
        for root, dirs, filenames in os.walk(dname):
            for filename in filenames:
                if filename.endswith(".mira"):
                    self.files.append(os.path.join(root, filename))

        if self.files:
            with open(self.files[0], 'rb') as in_stream:
                self.current.read(in_stream, self.files[0])

    def __bool__(self):
        return self.file_pos < len(self.files)

    def __iter__(self):
        return self

    def __next__(self):
        if not self:
            raise StopIteration
        result = self.current
        self.file_pos += 1
        if self.file_pos < len(self.files):
            with open(self.files[self.file_pos], 'rb') as in_stream:
                self.current.read(in_stream, self.files[self.file_pos])
        return result

    def __getitem__(self, index):
        if index >= len(self.files) or index < 0:
            raise IndexError("Index out of range")
        with open(self.files[index], 'rb') as in_stream:
            self.current.read(in_stream, self.files[index])
        return self.current