# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

"""
ShapeResults.py

Created on: Aug 10, 2015
Author: dkoes

Implements shapedb results interface for putting hits into a corresponder queue
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import threading

class PharmerDatabaseSearcher:
    pass  # Placeholder for the actual implementation

class CorrespondenceResult:
    pass  # Placeholder for the actual implementation

class CorAllocator:
    def allocate(self) -> CorrespondenceResult:
        return CorrespondenceResult()

class QueryParameters:
    pass  # Placeholder for the actual implementation

class ShapeConstraints:
    pass  # Placeholder for the actual implementation

class PharmaPoint:
    pass  # Placeholder for the actual implementation

class RMSDResult:
    pass  # Placeholder for the actual implementation

class Results(ABC):
    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def add(self, data: bytes, score: float) -> None:
        pass

    @abstractmethod
    def reserve(self, n: int) -> None:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def stopEarly(self) -> bool:
        pass

class ShapeResults(Results):
    def __init__(self, dbptr: PharmerDatabaseSearcher, querypoints: List[PharmaPoint],
                 resultQ: ThreadPoolExecutor, alloc: CorAllocator,
                 qp: QueryParameters, cons: ShapeConstraints, whichdb: int, totaldb: int, stopEarly: bool):
        self.dbptr = dbptr
        self.resultQ = resultQ
        self.alloc = alloc
        self.qparams = qp
        self.points = querypoints  # pharmacophore query points after alignment to grid

        self.db = whichdb
        self.numdb = totaldb
        self.defaultR = RMSDResult()  # all molecules have same transformation
        self.stop = stopEarly

    def clear(self) -> None:
        pass  # meaningless

    def add(self, data: bytes, score: float) -> None:
        # Placeholder for adding results to the queue
        result = self.alloc.allocate()
        # Process data and score to populate result
        self.resultQ.submit(lambda: result)

    def reserve(self, n: int) -> None:
        pass

    def size(self) -> int:
        return 0  # Placeholder for actual implementation

    def stopEarly(self) -> bool:
        return self.stop