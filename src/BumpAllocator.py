import threading

class BumpAllocator:
    def __init__(self, chunk_size=4096, thread_safe=True):
        self.chunks = []
        self.lock = threading.Lock() if thread_safe else None
        self.chunk = bytearray(chunk_size)
        self.offset = 0
        self.chunks.append(self.chunk)

    def __del__(self):
        self.clear()

    def clear(self):
        for chunk in self.chunks:
            del chunk
        self.chunks.clear()
        self.offset = len(self.chunk)  # force new allocation

    @property
    def num_chunks(self):
        return len(self.chunks)

    def alloc(self, size):
        if self.lock:
            with self.lock:
                return self._alloc(size)
        else:
            return self._alloc(size)

    def _alloc(self, size):
        if self.offset + size >= len(self.chunk):
            # need new chunk
            self.chunk = bytearray(len(self.chunk))
            self.chunks.append(self.chunk)
            self.offset = 0
        ptr = self.chunk[self.offset:self.offset + size]
        self.offset += size
        return ptr

# Example usage:
if __name__ == "__main__":
    allocator = BumpAllocator(chunk_size=1024, thread_safe=True)
    block1 = allocator.alloc(64)
    block2 = allocator.alloc(128)
    print(f"Number of chunks: {allocator.num_chunks}")