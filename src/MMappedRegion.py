import os
import mmap
import sys

class MMappedRegion:
    def __init__(self, fname=None, readOnly=False):
        self.data = None
        self.size = 0
        if fname is not None:
            self.map(fname, readOnly)

    def __del__(self):
        self.clear()

    def clear(self):
        if self.data is not None:
            self.data.close()
        self.data = None
        self.size = 0

    def map(self, fname, readOnly, sequential=True, populate=False, readonce=False):
        if self.data is not None:
            self.data.close()
        
        flags = os.O_RDONLY if readOnly else (os.O_RDWR | os.O_CREAT)
        fd = os.open(fname, flags)
        if fd < 0:
            print(f"Error opening file {fname}", file=sys.stderr)
            sys.exit(1)

        try:
            if sequential:
                os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_SEQUENTIAL)
            if readonce:
                os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_NOREUSE)
            
            prot = mmap.PROT_READ if readOnly else (mmap.PROT_READ | mmap.PROT_WRITE)
            access = mmap.ACCESS_PRIVATE if readOnly else mmap.ACCESS_WRITE
            self.size = os.path.getsize(fname)
            self.data = mmap.mmap(fd, self.size, prot=prot, access=access)
        finally:
            os.close(fd)

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        assert self.size % 4 == 0
        return self.size // 4

    def begin(self):
        return self.data

    def end(self):
        return self.data + len(self)

    def sync(self):
        self.data.flush()

# Example usage:
# region = MMappedRegion("example.bin", readOnly=True)
# print(region[0])