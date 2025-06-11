import threading

class SPSCQueue:
    def __init__(self, N):
        self.buffer = [None] * N
        self.pread = 0
        self.padding = [0] * 15
        self.pwrite = 0
        self.padding2 = [0] * 15
        self.done = False

    def clear_and_destroy(self):
        for i in range(len(self.buffer)):
            if self.buffer[i]:
                del self.buffer[i]
                self.buffer[i] = None
        self.done = False
        self.pread = self.pwrite = 0

    def push(self, val):
        if val is None:
            return False

        if self.buffer[self.pwrite] is None:
            # memory barrier necessary here if stores become visible out of order
            self.buffer[self.pwrite] = val
            self.pwrite = (self.pwrite + 1) % len(self.buffer)
            return True
        return False

    def pop(self):
        if self.buffer[self.pread] is None:
            return False, None
        val = self.buffer[self.pread]
        self.buffer[self.pread] = None
        self.pread = (self.pread + 1) % len(self.buffer)
        return True, val

    def empty(self):
        return self.buffer[self.pread] is None and self.done

    def set_done(self):
        self.done = True

class SPSCDataQueue:
    class Node:
        def __init__(self):
            self.val = None
            self.isEmpty = True

    def __init__(self, N):
        self.buffer = [self.Node() for _ in range(N)]
        self.pread = 0
        self.padding = [0] * 15
        self.pwrite = 0
        self.padding2 = [0] * 15
        self.done = False

    def push(self, val):
        while True:
            if self.buffer[self.pwrite].isEmpty:
                # memory barrier necessary here if stores become visible out of order
                self.buffer[self.pwrite].val = val
                self.buffer[self.pwrite].isEmpty = False
                if self.pwrite >= len(self.buffer) - 1:
                    self.pwrite = 0
                else:
                    self.pwrite += 1
                return
            threading.yield_
            threading.interrupt_main()

    def pop(self):
        if self.buffer[self.pread].isEmpty:
            return False, None
        val = self.buffer[self.pread].val
        self.buffer[self.pread].isEmpty = True
        if self.pread >= len(self.buffer) - 1:
            self.pread = 0
        else:
            self.pread += 1
        return True, val

    def top(self):
        if self.buffer[self.pread].isEmpty:
            return None
        return self.buffer[self.pread].val

    def empty(self):
        return self.buffer[self.pread].isEmpty and self.done

    def set_done(self):
        self.done = True