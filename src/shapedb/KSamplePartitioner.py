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
KSamplePartitioner.py

Created on: Oct 17, 2011
Author: dkoes
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class DataViewer:
    pass  # Placeholder for DataViewer class

class MappableOctTree:
    pass  # Placeholder for MappableOctTree class

class TopDownPartitioner(ABC):
    def __init__(self, dv: Optional[DataViewer] = None):
        self.dv = dv

    @abstractmethod
    def create(self, dv: DataViewer) -> 'TopDownPartitioner':
        pass

    @abstractmethod
    def partition(self, parts: List['TopDownPartitioner']) -> None:
        pass

class KSamplePartitioner(TopDownPartitioner):
    class CenterChoice:
        AveCenter = 0
        MinMaxCenter = 1

    def __init__(self, kc: int = 8, ks: int = 5, centerFind: CenterChoice = CenterChoice.AveCenter, stop: int = 32768, dv: Optional[DataViewer] = None):
        super().__init__(dv)
        self.kcenters = kc
        self.ksamples = ks
        self.centerFind = centerFind
        self.stopPartitionSize = stop

    def kCluster(self, indices: List[int], clusters: List[List[int]]) -> None:
        # Placeholder for kCluster implementation
        pass

    def getCenter(self, cluster: List[int], MIV: Optional[MappableOctTree], MSV: Optional[MappableOctTree]) -> None:
        # Placeholder for getCenter implementation
        pass

    def fitKCenterToSize(self, n: int) -> int:
        # Placeholder for fitKCenterToSize implementation
        return 0

    def create(self, dv: DataViewer) -> 'TopDownPartitioner':
        return KSamplePartitioner(dv=dv, kc=self.kcenters, ks=self.ksamples, centerFind=self.centerFind, stop=self.stopPartitionSize)

    def partition(self, parts: List['TopDownPartitioner']) -> None:
        # Placeholder for partition implementation
        pass