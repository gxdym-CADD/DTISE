# workfile.py
#
# Simple wrapper for a file that is written to and then memory mapped.
import os
import mmap

class WorkFile:
    def __init__(self):
        self.file = None
        self.map = None
        self.mapping = None

    def __del__(self):
        self.remove()

    def set(self, name):
        if self.file is not None:
            self.file.close()
        self.file = open(name, 'w+b')

    def switchToMap(self):
        if self.file is not None:
            self.file.flush()
            self.mapping = mmap.mmap(self.file.fileno(), 0)
            self.map = self.mapping
            self.file.close()
            self.file = None

    def clear(self):
        if self.file is not None:
            self.file.truncate(0)
        elif self.mapping is not None:
            self.mapping.seek(0)
            self.mapping.write(b'')
            self.mapping.flush()

    def remove(self):
        if self.file is not None:
            self.file.close()
            os.remove(self.file.name)
            self.file = None
        if self.mapping is not None:
            self.mapping.close()
            os.remove(self.mapping.name)
            self.mapping = None

# Example usage:
# wf = WorkFile()
# wf.set("example.txt")
# wf.file.write(b"Hello, World!")
# wf.switchToMap()
# print(wf.map.read(13))  # Output: b'Hello, World!'
# wf.clear()
# wf.remove()