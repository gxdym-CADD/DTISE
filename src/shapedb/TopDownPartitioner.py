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
TopDownPartitioner.py

Created on: Oct 18, 2011
Author: dkoes
"""

from abc import ABC, abstractmethod
from typing import List

class DataViewer:
    def size(self) -> int:
        pass

class TopDownPartitioner(ABC):
    def __init__(self, data: DataViewer = None):
        self.data = data
        self.indices: List[int] = []

    @abstractmethod
    def create(self, dv: DataViewer) -> 'TopDownPartitioner':
        pass

    @abstractmethod
    def partition(self, parts: List['TopDownPartitioner']) -> None:
        pass

    def size(self) -> int:
        return len(self.indices)

    def get_data(self) -> DataViewer:
        return self.data

    def extract_indices(self, ind: List[int]) -> None:
        ind.clear()
        ind.extend(self.indices)
        self.indices.clear()

    def init_from_data(self):
        self.indices = list(range(self.data.size()))