import os
import mmap

class MemMapped:
    def __init__(self):
        self.addr = None
        self.sz = 0

    def map(self, fname, readOnly=True, sequential=False, populate=False, readonce=False):
        try:
            with open(fname, 'rb' if readOnly else 'r+b') as f:
                self.sz = os.path.getsize(fname)
                flags = mmap.ACCESS_READ if readOnly else mmap.ACCESS_WRITE
                self.addr = mmap.mmap(f.fileno(), 0, access=flags)
                return True
        except Exception as e:
            print(f"Error mapping file: {e}")
            return False

    def __getitem__(self, i):
        return self.addr[i]

    def __bytes__(self):
        return self.addr

    def begin(self):
        return self.addr.tobytes()

    def end(self):
        return self.addr[self.sz:]

    def clear(self):
        if self.addr:
            self.addr.close()
            self.addr = None
            self.sz = 0

    def size(self):
        return self.sz