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

"""
GSSTypes.py

Created on: Oct 18, 2011
Author: dkoes

Simple types used by GSSTrees
"""

from typing import List, Tuple
import os

file_index = int

class result_info:
    def __init__(self, p: file_index = 0, v: float = 0.0):
        self.pos = p  # position of result
        self.val = v  # some measure of goodness of result

    # sort by position for better access
    def __lt__(self, rhs: 'result_info') -> bool:
        return self.pos < rhs.pos

class DataViewer:
    pass

class Cluster:
    pass