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
Results.py

Created on: Jun 3, 2013
Author: dkoes

Base class for results containers. Default behavior is to do nothing at all.
"""

from abc import ABC, abstractmethod
from typing import List

class Results(ABC):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def add(self, data: bytes, score: float) -> None:
        pass

    def reserve(self, n: int) -> None:
        pass

    def size(self) -> int:
        return 0

    def stopEarly(self) -> bool:
        return False

# For objects that just store a string identifier (null terminated)
class StringResults(Results):
    def __init__(self):
        self.strs: List[str] = []
        self.scores: List[float] = []

    def clear(self) -> None:
        self.strs.clear()
        self.scores.clear()

    def add(self, data: bytes, score: float) -> None:
        # Assuming data is null-terminated and encoded in UTF-8
        self.strs.append(data.decode('utf-8').rstrip('\0'))
        self.scores.append(score)

    def reserve(self, n: int) -> None:
        self.strs.reserve(n)
        self.scores.reserve(n)

    def size(self) -> int:
        return len(self.strs)

    def getString(self, i: int) -> str:
        return self.strs[i]

    def getScore(self, i: int) -> float:
        return self.scores[i]