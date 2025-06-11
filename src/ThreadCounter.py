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

import threading

class ThreadCounter:
    def __init__(self, n):
        self.maxThreads = n
        self.count = 0
        self.lock = threading.Lock()

    # return true if there's an available thread
    # it is assumed the caller will then spawn a thread and call reduceThreadCount
    def threadAvailable(self):
        with self.lock:
            if self.count < self.maxThreads:
                self.count += 1
                return True
            else:
                return False

    def reduceThreadCount(self):
        with self.lock:
            self.count -= 1