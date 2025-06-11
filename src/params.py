import json
from enum import Enum
from typing import List, Optional

class SortType(Enum):
    Undefined = 0
    RMSD = 1
    MolWeight = 2
    NRBnds = 3

SortTyp = SortType

class PropFilter:
    def __init__(self, kind: int, min_val: float = -float('inf'), max_val: float = float('inf')):
        self.kind = kind
        self.min = min_val
        self.max = max_val

class QueryParameters:
    def __init__(self):
        self.maxRMSD = float('inf')
        self.reduceConfs = 2**32 - 1
        self.orientationsPerConf = 2**32 - 1
        self.maxHits = 2**32 - 1
        self.sort = SortType.Undefined
        self.reverseSort = False
        self.minWeight = 0
        self.maxWeight = 2**32 - 1
        self.reducedMinWeight = 0
        self.reducedMaxWeight = 2**32 - 1
        self.minRot = 0
        self.maxRot = 2**32 - 1
        self.isshape = False
        self.subset = ""
        self.propfilters: List[PropFilter] = []

    def addPropFilter(self, p: int, name: str, data: dict):
        min_key = f"min{name}"
        max_key = f"max{name}"

        if min_key in data and isinstance(data[min_key], (int, float)) or max_key in data and isinstance(data[max_key], (int, float)):
            f = PropFilter(p)
            if min_key in data:
                f.min = data[min_key]
            if max_key in data:
                f.max = data[max_key]
            self.propfilters.append(f)

    def from_json(self, data: dict):
        if "maxRMSD" in data and isinstance(data["maxRMSD"], (int, float)):
            self.maxRMSD = data["maxRMSD"]
        if "reduceConfs" in data and isinstance(data["reduceConfs"], int):
            self.reduceConfs = data["reduceConfs"]

        if "max-hits" in data and isinstance(data["max-hits"], int):
            self.maxHits = data["max-hits"]
        if "max-orient" in data and isinstance(data["max-orient"], int):
            self.orientationsPerConf = data["max-orient"]

        if "minMolWeight" in data and isinstance(data["minMolWeight"], (int, float)):
            self.minWeight = data["minMolWeight"]
            self.reducedMinWeight = ThreePointData.reduceWeight(self.minWeight)
        if "maxMolWeight" in data and isinstance(data["maxMolWeight"], (int, float)):
            self.maxWeight = data["maxMolWeight"]
            self.reducedMaxWeight = ThreePointData.reduceWeight(self.maxWeight)

        if "minrotbonds" in data and isinstance(data["minrotbonds"], int):
            self.minRot = ThreePointData.reduceRotatable(data["minrotbonds"])
        if "maxrotbonds" in data and isinstance(data["maxrotbonds"], int):
            self.maxRot = data["maxrotbonds"]

        if "subset" in data and isinstance(data["subset"], str):
            self.subset = data["subset"]

        if "ShapeModeSelect" in data and isinstance(data["ShapeModeSelect"], str) and data["ShapeModeSelect"] == "search":
            self.isshape = True

        self.sort = SortType.RMSD
        self.reverseSort = self.isshape

        self.addPropFilter(MolProperties.LogP, "logp", data)
        self.addPropFilter(MolProperties.PSA, "psa", data)
        self.addPropFilter(MolProperties.NAromatics, "aromatics", data)
        self.addPropFilter(MolProperties.HBA, "hba", data)
        self.addPropFilter(MolProperties.HBD, "hbd", data)

class DataParameters:
    def __init__(self):
        self.start = 0
        self.num = 0
        self.sort: Optional[SortType] = None

# Assuming ThreePointData and MolProperties are defined elsewhere
class DataParameters:
    def __init__(self):
        self.start = 0
        self.num = 0
        self.sort = None  # Assuming SortType is an enum or similar, use None as default

# Assuming ThreePointData and MolProperties are defined elsewhere
from typing import Optional

class DataParameters:
    def __init__(self):
        self.start: int = 0
        self.num: int = 0
        self.sort: Optional[SortType] = None
        self.reverse_sort: bool = False
        self.extra_info: bool = False
        self.draw_code: int = 0

# Assuming SortType, ThreePointData, and MolProperties are defined elsewhere