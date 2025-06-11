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
pharmarec.py

Created on: July 30, 2010
Author: dkoes

Routines for pharmacophore recognition.
"""

import json
from typing import List, Optional, Callable, Dict
from openbabel import pybel, OBConversion, OBSmartsPattern, Vector3

THRESHOLD = 0.0001

class PharmaPoint:
    pass

genPointVectorFn = Callable[[List[int], pybel.Molecule, PharmaPoint], None]

class PharmaInteract:
    def __init__(self, complement: int = 0, maxDist: float = 0.0, minMatch: int = 0):
        self.complement = complement
        self.maxDist = maxDist
        self.minMatch = minMatch

class Pharma:
    def __init__(self, indx: int = -1, n: Optional[str] = None, sm: Optional[List[str]] = None,
                 atomic: int = 0, r: float = 0.5, cl: float = 0.0, nb: int = 1, trfr: float = 0.0):
        self.name = n
        self.atomic_number_label = atomic
        self.index = indx
        self.smarts: List[OBSmartsPattern] = []
        self.defaultSearchRadius = r
        self.getVectors: Optional[genPointVectorFn] = None
        self.clusterLimit = cl

        if sm is not None:
            for s in sm:
                pattern = OBSmartsPattern()
                pattern.Init(s)
                self.smarts.append(pattern)

        self.setVectorFn()

    def setVectorFn(self, fn: Optional[genPointVectorFn] = None):
        pass

    def __eq__(self, other):
        return (self.name == other.name and
                self.atomic_number_label == other.atomic_number_label and
                self.index == other.index and
                self.defaultSearchRadius == other.defaultSearchRadius and
                self.clusterLimit == other.clusterLimit)

    def __ne__(self, other):
        return not self == other

class Pharmas:
    def __init__(self, ps: Optional[List[Pharma]] = None):
        self.pharmas: List[Pharma] = []
        self.numPharmas = 0
        self.nameLookup: Dict[str, int] = {}

        if ps is not None:
            self.initialize(ps)

    def initialize(self, ps: List[Pharma]):
        self.pharmas = ps.copy()
        self.numPharmas = len(ps)
        for i, pharma in enumerate(ps):
            self.nameLookup[pharma.name] = i

    def __getitem__(self, i: int) -> Pharma:
        return self.pharmas[i]

    def __eq__(self, other):
        return (self.pharmas == other.pharmas and
                self.numPharmas == other.numPharmas and
                self.nameLookup == other.nameLookup)

    def __ne__(self, other):
        return not self == other

    def size(self) -> int:
        return self.numPharmas

    def pharmaFromName(self, name: str) -> Optional[Pharma]:
        if name in self.nameLookup:
            return self.pharmas[self.nameLookup[name]]
        return None

    def setDefaultSearchRadius(self, val: float = 1.0):
        for pharma in self.pharmas:
            pharma.defaultSearchRadius = val
import math
from typing import List, Optional, Tuple

class Pharma:
    def __init__(self, name: str):
        self.name = name
        self.defaultSearchRadius = 1.0

class Pharmas:
    def __init__(self, pharmas: List[Pharma], name_lookup: dict):
        self.pharmas = pharmas
        self.num_pharmas = len(pharmas)
        self.name_lookup = name_lookup

    def __getitem__(self, i: int) -> Optional[Pharma]:
        if 0 <= i < self.num_pharmas:
            return self.pharmas[i]
        return None

    def __eq__(self, other):
        if not isinstance(other, Pharmas):
            return False
        return (self.num_pharmas == other.num_pharmas and
                self.name_lookup == other.name_lookup)

    def __ne__(self, other):
        return not self == other

    def size(self) -> int:
        return self.num_pharmas

    def pharma_from_name(self, name: str) -> Optional[Pharma]:
        if name in self.name_lookup:
            return self.pharmas[self.name_lookup[name]]
        return None

    def set_default_search_radius(self, val: float = 1.0):
        for pharma in self.pharmas:
            pharma.defaultSearchRadius = val

class PharmaPoint:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, pharma: Optional[Pharma] = None):
        self.x = x
        self.y = y
        self.z = z
        self.size = 0
        self.pharma = pharma
        self.radius = pharma.defaultSearchRadius if pharma else 0
        self.vecpivot = 0.0
        self.requirements = 'Required'
        self.minSize = 0
        self.maxSize = 0

    def radius_weight(self) -> float:
        return 1.0 / (self.radius * self.radius)

    def same_location(self, rhs: 'PharmaPoint') -> bool:
        THRESHOLD = 1e-6
        if abs(self.x - rhs.x) > THRESHOLD:
            return False
        if abs(self.y - rhs.y) > THRESHOLD:
            return False
        if abs(self.z - rhs.z) > THRESHOLD:
            return False
        return True

    def requirement_str(self) -> str:
        match self.requirements:
            case 'Required':
                return "required"
            case 'Optional':
                return "optional"
            case 'NotPresent':
                return "notpresent"
            case _:
                return ""

    @staticmethod
    def pharma_dist(a: 'PharmaPoint', b: 'PharmaPoint') -> float:
        SQR = lambda x: x * x
        return math.sqrt(SQR(a.x - b.x) + SQR(a.y - b.y) + SQR(a.z - b.z))

    def __str__(self):
        return f"PharmaPoint(x={self.x}, y={self.y}, z={self.z}, pharma={self.pharma.name if self.pharma else None})"

# Example usage
pharmas = Pharmas([Pharma("Pharma1"), Pharma("Pharma2")], {"Pharma1": 0, "Pharma2": 1})
point = PharmaPoint(1.0, 2.0, 3.0, pharmas[0])
print(point)