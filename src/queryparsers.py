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

import json
from typing import List, Optional
from io import TextIOBase

class QueryParser:
    def parse(self, pharmas: 'Pharmas', in_stream: TextIOBase, points: List['PharmaPoint'], excluder: 'ShapeConstraints') -> bool:
        raise NotImplementedError("Subclasses must implement this method")

class TextQueryParser(QueryParser):
    def parse(self, pharmas: 'Pharmas', in_stream: TextIOBase, points: List['PharmaPoint'], excluder: 'ShapeConstraints') -> bool:
        points.clear()
        line = in_stream.readline().strip()
        while line.startswith('#'):
            line = in_stream.readline().strip()

        if line.startswith('<'):  # assume ligbuilder
            while True:
                line = in_stream.readline().strip()
                if line.startswith('<End>'):
                    break

                if line.startswith('<Feature_description>'):
                    while True:
                        line = in_stream.readline().strip()
                        if line.startswith('<'):
                            break
                        tokens = line.split()
                        if len(tokens) > 5:
                            pharma_type = None
                            # set pharma type
                            if tokens[2][0] == 'D':
                                pharma_type = pharmas.pharmaFromName("HydrogenDonor")
                            elif tokens[2][0] == 'A':
                                pharma_type = pharmas.pharmaFromName("HydrogenAcceptor")
                            elif tokens[2][0] == 'H':
                                pharma_type = pharmas.pharmaFromName("Hydrophobic")

                            if pharma_type:
                                x = float(tokens[3])
                                y = float(tokens[4])
                                z = float(tokens[5])

                                p = PharmaPoint(x, y, z, pharma_type)
                                points.append(p)
        else:
            p = PharmaPoint()
            while p.read(pharmas, in_stream):
                points.append(p)

        return len(points) > 0

class JSonQueryParser(QueryParser):
    def parse(self, pharmas: 'Pharmas', in_stream: TextIOBase, points: List['PharmaPoint'], excluder: 'ShapeConstraints') -> bool:
        try:
            points.clear()
            excluder.clear()

            root = json.load(in_stream)
            if not readPharmaPointsJSON(pharmas, root, points):
                return False
            return excluder.readJSONExclusion(root)
        except Exception as e:
            return False

class PH4Parser(QueryParser):
    def getPharma(self, moename: str, pharmas: 'Pharmas') -> Optional['Pharma']:
        length = len(moename)
        if length < 3:
            return None
        if moename[0] == 'D':  # donor
            if moename[1] != 'o' or moename[2] != 'n':
                return None
            if length > 3 and moename[3] == '2':  # projected point, not yet supported
                return None
            return pharmas.pharmaFromName("HydrogenDonor")
        elif moename[0] == 'A':  # acceptor or aromatic or anion
            if moename[1] == 'c':
                # acceptor
                if moename[2] != 'c':
                    return None
                if length > 3 and moename[3] == '2':  # projected point, not yet supported
                    return None
                return pharmas.pharmaFromName("HydrogenAcceptor")
            elif moename[1] == 'r':
                # aromatic
                if moename[2] != 'o':
                    return None
                return pharmas.pharmaFromName("Aromatic")
            elif moename[1] == 'n':
                # anion (neg)
                if moename[2] != 'i':
                    return None
                return pharmas.pharmaFromName("NegativeIon")
            else:
                return None
class MOEParser:
    def get_pharma(self, moename: str, pharmas: 'Pharmas') -> Optional['Pharma']:
        if not moename or len(moename) < 3:
            return None

        if moename[0] == 'a':
            # acceptor
            if moename[1] != 'c':
                return None
            return pharmas.pharma_from_name("HydrogenAcceptor")
        elif moename[1] == 'r':
            # aromatic
            if moename[2] != 'o':
                return None
            return pharmas.pharma_from_name("Aromatic")
        elif moename[1] == 'n':
            # anion (neg)
            if moename[2] != 'i':
                return None
            return pharmas.pharma_from_name("NegativeIon")
        else:
            return None

    def parse(self, pharmas: 'Pharmas', in_stream: TextIO, points: List['PharmaPoint'], excluder: 'ShapeConstraints') -> bool:
        points.clear()
        
        # first #moe
        line = in_stream.readline().strip()
        if not line or line[:4] != "#moe":
            return False
        
        # then #pharmacophore
        line = in_stream.readline().strip()
        
        # then scheme
        line = in_stream.readline().strip()
        
        # then look for #feature, number of points
        before_dummies = 0
        after_dummies = 0
        while True:
            line = in_stream.readline().strip()
            if not line or line[:8] == "#feature":
                tokens = line.split()
                start = 0
                end = 0
                for i, token in enumerate(tokens[:-1]):
                    if token == "x":
                        start = i
                    if token == "r":  # r is both a label of radius and type
                        end = i
                before_dummies = (start - 4) // 2  # hard code feature num expr tt
                after_dummies = len(tokens) - end - 1
                break
        
        while True:
            line = in_stream.readline().strip()
            if not line or line == "#volumesphere":
                break
            
            tokens = line.split()
            point = PharmaPoint()
            x, y, z, r = map(float, tokens[:4])
            point.x, point.y, point.z, point.radius = x, y, z, r
            
            types = [self.get_pharma(token, pharmas) for token in tokens[4:]]
            for pharma_type in types:
                if pharma_type is not None:
                    point.pharma = pharma_type
                    points.append(point)
        
        if line == "#volumesphere":
            num_spheres = int(in_stream.readline().strip())
            for _ in range(num_spheres):
                x, y, z, r = map(float, in_stream.readline().split())
                excluder.add_exclusion_sphere(x, y, z, r)
                excluder.enable_exclusion_spheres()
        
        return True

class PMLParser:
    def parse(self, pharmas: 'Pharmas', in_stream: TextIO, points: List['PharmaPoint'], excluder: 'ShapeConstraints') -> bool:
        from xml.etree import ElementTree as ET
        
        points.clear()
        tree = ET.parse(in_stream)
        root = tree.getroot()
        
        base = root.find("MolecularEnvironment")
        if base is None:
            base = root
            ph = base.find("pharmacophore")
        else:
            ph = base.find("pharmacophore")
        
        if ph is None:
            # do a more exhaustive search
            for elem in root.iter():
                if elem.tag == "pharmacophore":
                    ph = elem
                    break
        
        if ph is None:
            return False
        
        # parse pharmacophore points and exclusion spheres
        # (this part would need to be completed based on the specific XML structure)
        
        return True
import xml.etree.ElementTree as ET

class FindPharmVisitor:
    def __init__(self):
        self.ph = None

    def visit(self, elem):
        if elem.tag == "pharmacophore":
            self.ph = elem
            return True
        for child in elem:
            if self.visit(child):
                break
        return False

def parse_pharmacophore(doc, base=None):
    if base is None:
        ph = doc.find("pharmacophore")
    else:
        ph = base.find("pharmacophore")

    if ph is None:
        # do a more exhaustive search
        visit = FindPharmVisitor()
        ET.ElementTree(doc).iterparse(events=("start",))
        ph = visit.ph

        if ph is None:
            return False

    points = []
    for pt in ph.iter():
        el = pt
        if el.tag == "pharmacophore":
            continue
        n = el.get("name")  # short name
        if n:
            point = {}
            if el.get("optional") == "true":
                point["requirements"] = "Optional"

            switch_cases = {
                'H': lambda: parse_hydrogen(el, point),
                'P': lambda: parse_ion(el, point, "PositiveIon"),
                'N': lambda: parse_ion(el, point, "NegativeIon"),
                'A': lambda: parse_aromatic(el, point)
            }

            switch_case = switch_cases.get(n[0])
            if switch_case:
                switch_case()

    return points

def parse_hydrogen(el, point):
    if n[1] == 'B':  # hydrogen bond
        if n[2] == 'A':
            point["pharma"] = "HydrogenAcceptor"
        elif n[2] == 'D':
            point["pharma"] = "HydrogenDonor"
        else:
            return

        toligand = el.get("pointsToLigand") == "true"
        orig = el.find("target" if toligand else "origin")
        if orig is None:
            pos = el.find("position")
            if pos is not None:
                point["x"] = float(pos.get("x3"))
                point["y"] = float(pos.get("y3"))
                point["z"] = float(pos.get("z3"))
                point["radius"] = float(pos.get("tolerance"))
        else:
            point["x"] = float(orig.get("x3"))
            point["y"] = float(orig.get("y3"))
            point["z"] = float(orig.get("z3"))
            point["radius"] = float(orig.get("tolerance"))

            targ = el.find("target" if not toligand else "origin")
            if targ is not None:
                vec = vector3(float(targ.get("x3")), float(targ.get("y3")), float(targ.get("z3")))
                vec -= vector3(point["x"], point["y"], point["z"])
                t = float(targ.get("tolerance"))
                point["vecpivot"] = atan2(t, vec.length())
                point["vecs"].append(vec)

def parse_ion(el, point, ion_type):
    if n[1] == 'I':
        pos = el.find("position")
        if pos is not None:
            point["pharma"] = ion_type
            point["x"] = float(pos.get("x3"))
            point["y"] = float(pos.get("y3"))
            point["z"] = float(pos.get("z3"))
            point["radius"] = float(pos.get("tolerance"))

def parse_aromatic(el, point):
    if n[1] == 'R':
        pos = el.find("position")
        if pos is not None:
            point["pharma"] = "Aromatic"
            point["x"] = float(pos.get("x3"))
            point["y"] = float(pos.get("y3"))
            point["z"] = float(pos.get("z3"))
            point["radius"] = float(pos.get("tolerance"))

            norm = el.find("normal")
            if norm is not None:
                vec = vector3(float(norm.get("x3")), float(norm.get("y3")), float(norm.get("z3")))
                vec -= vector3(point["x"], point["y"], point["z"])
                t = float(norm.get("tolerance"))
                point["vecpivot"] = atan2(t, vec.length())
                point["vecs"].append(vec)

            if el.get("optional") == "true":
                point["requirements"] = "Optional"
from typing import List, Dict, Optional
import math

class vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __sub__(self, other: 'vector3') -> 'vector3':
        return vector3(self.x - other.x, self.y - other.y, self.z - other.z)

class PharmaPoint:
    Optional = "Optional"

    def __init__(self):
        self.name = ""
        self.vecpivot = 0.0
        self.vecs: List[vector3] = []
        self.requirements = ""

class Excluder:
    def addExclusionSphere(self, x: float, y: float, z: float, r: float) -> None:
        pass

    def enableExclusionSpheres(self) -> None:
        pass

class QueryParsers:
    @staticmethod
    def parseQuery(xml_content: str, excluder: Excluder) -> bool:
        from xml.etree import ElementTree as ET

        root = ET.fromstring(xml_content)
        points: List[Dict[str, any]] = []

        for el in root.findall(".//point"):
            point = {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "radius": 0.0,
                "pharma": None,
                "vecpivot": 0.0,
                "vecs": [],
                "requirements": ""
            }

            pos = el.find("position")
            if pos is not None:
                point["x"] = float(pos.get("x3"))
                point["y"] = float(pos.get("y3"))
                point["z"] = float(pos.get("z3"))
                point["radius"] = float(pos.get("tolerance"))

                norm = el.find("normal")
                if norm is not None:
                    vec = vector3(float(norm.get("x3")), float(norm.get("y3")), float(norm.get("z3")))
                    vec -= vector3(point["x"], point["y"], point["z"])
                    t = float(norm.get("tolerance"))
                    point["vecpivot"] = math.atan2(t, vec.length())
                    point["vecs"].append(vec)

                if el.get("optional") == "true":
                    point["requirements"] = PharmaPoint.Optional

                points.append(point)
            else:
                n = el.get("type")
                if n and n == "exclusion" and el.text == "volume":
                    pos = el.find("position")
                    if pos:
                        x = float(pos.get("x3"))
                        y = float(pos.get("y3"))
                        z = float(pos.get("z3"))
                        r = float(pos.get("tolerance"))
                        excluder.addExclusionSphere(x, y, z, r)
                        excluder.enableExclusionSpheres()

        newpoints: List[Dict[str, any]] = []
        merged: List[bool] = [False] * len(points)

        for i in range(len(points)):
            if merged[i]:
                continue
            if points[i]["pharma"].name == "HydrogenAcceptor" or points[i]["pharma"].name == "HydrogenDonor":
                for j in range(i + 1, len(points)):
                    vecs = points[i]["vecs"]
                    if (points[i]["x"] == points[j]["x"] and
                        points[i]["y"] == points[j]["y"] and
                        points[i]["radius"] == points[j]["radius"] and
                        points[i]["z"] == points[j]["z"] and
                        points[i]["pharma"].name == points[j]["pharma"].name):
                        merged[j] = True
                        vecs.extend(points[j]["vecs"])

                if len(vecs) > 0:
                    vec = vector3(0, 0, 0)
                    for v in range(len(vecs)):
                        vec += vecs[v]
                    vec /= len(vecs)
                    points[i]["vecs"].clear()
                    points[i]["vecs"].append(vec)

            newpoints.append(points[i])

        points[:] = newpoints
        return True

# Example usage:
# excluder = Excluder()
# xml_content = "<root>...</root>"
# success = QueryParsers.parseQuery(xml_content, excluder)