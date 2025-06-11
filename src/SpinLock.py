# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

class SpinMutexEnum:
    SpinMutexUnlocked = 0
    SpinMutexLocked = 1

class SpinMutex:
    def __init__(self, v=SpinMutexEnum.SpinMutexUnlocked):
        self.prevent_false_sharing = [0] * 7
        self.val = v
        self.prevent_false_sharing_after = [0] * 8

class SpinLock:
    def __init__(self, m: SpinMutex, lock=True):
        self.mutex = m
        self.holdsLock = False
        if lock:
            self.acquire()
        self.holdsLock = lock

    def acquire(self):
        while not self.__sync_bool_compare_and_swap():
            pass  # spin if was already locked
        assert self.mutex.val == SpinMutexEnum.SpinMutexLocked

    def release(self):
        assert self.mutex.val == SpinMutexEnum.SpinMutexLocked
        self.mutex.val = SpinMutexEnum.SpinMutexUnlocked

    def __sync_bool_compare_and_swap(self):
        # Simulating atomic compare and swap using a lock
        if self.mutex.val == SpinMutexEnum.SpinMutexUnlocked:
            self.mutex.val = SpinMutexEnum.SpinMutexLocked
            return True
        return False

    def __del__(self):
        # always release if we're holding the lock
        if self.holdsLock:
            self.release()