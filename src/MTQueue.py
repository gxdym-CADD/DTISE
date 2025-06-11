import threading
from collections import deque

class SpinLock:
    def __init__(self, lock, acquire=True):
        self.lock = lock
        if acquire:
            self.lock.acquire()

    def release(self):
        self.lock.release()

class MTQueue:
    def __init__(self, max_size=0):
        self.data = deque()
        self.mutex = threading.Lock()
        self.registered_producers = 0
        self.num = 0
        self.max_size = max_size

    def add_producer(self):
        with self.mutex:
            self.registered_producers += 1

    def remove_producer(self):
        with self.mutex:
            assert self.registered_producers > 0
            self.registered_producers -= 1

    def num_producers(self):
        return self.registered_producers

    def set_max(self, m):
        with self.mutex:
            self.max_size = m

    def size(self):
        return self.num

    def push(self, val):
        lock = SpinLock(self.mutex, False)
        if self.max_size > 0:
            while True:
                while self.num >= self.max_size:
                    threading.yield_()
                lock.acquire()
                if self.num < self.max_size:
                    break
                lock.release()
        else:
            lock.acquire()

        with self.mutex:
            self.data.append(val)
            self.num += 1

    def pop(self, val):
        lock = SpinLock(self.mutex, False)
        while True:
            while self.num == 0:
                if self.registered_producers == 0 and self.num == 0:
                    return False
                threading.yield_()
            lock.acquire()
            if self.num != 0:
                break
            lock.release()

        with self.mutex:
            val[0] = self.data.popleft()
            self.num -= 1
            return True

    def finished(self):
        return self.registered_producers == 0 and self.num == 0

    def pop_all(self, val):
        lock = SpinLock(self.mutex, False)
        if self.num == 0:
            if self.finished():
                return False
            return True

        with self.mutex:
            val.extend(self.data)
            self.data.clear()
            self.num = 0
            return not self.finished()