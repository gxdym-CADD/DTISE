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
ReadMCMol.py

Created on: Feb 2, 2011
Author: dkoes
"""

from openbabel import pybel
import sys

class OBVecData:
    def __init__(self):
        self.value = []

    def GetValue(self):
        return self.value

class ReadMCMol:
    def __init__(self, infile, format_name, stride, offset, reduce, isgzip=False):
        self.infile = infile
        self.stride = stride
        self.offset = offset
        self.reduceConfs = reduce if reduce > 0 else float('inf')
        self.molcnt = 0
        self.pharmacophores = []
        self.conv = pybel.ob.OBConversion()
        self.conv.SetInFormat(format_name)
        self.conv.SetOutFormat("sdf")
        self.next = MInfo(self.infile, self.conv)
        self.next.load()

    def read(self, mol):
        mol.Clear()
        if not self.next.isValid():
            return False
        while self.next.isValid():
            if (self.molcnt % self.stride) == self.offset:
                self.molcnt += 1
                confcnt = 1
                mol = self.next.getMol()
                N = mol.NumAtoms()
                curtitle = self.next.title

                self.pharmacophores.clear()
                if self.next.pharmacophore:
                    self.pharmacophores.append(self.next.pharmacophore)

                while self.next.load():
                    if self.next.title == curtitle:
                        if confcnt < self.reduceConfs:
                            if self.next.getMol().NumAtoms() != N:
                                sys.stderr.write("Warning: Invalid Input. Sequential molecules with the same name should be conformers.\n")
                                break
                            confdata = list(self.next.getMol().GetConformer(0))
                            mol.AddConformer(confdata)
                            if self.pharmacophores:
                                self.pharmacophores.append(self.next.pharmacophore)
                        confcnt += 1
                    else:
                        break

                if self.pharmacophores:
                    sddata = OBVecData()
                    # Assuming some operation to add pharmacophores to sddata
                    pass
            return True
        return False

class MInfo:
    def __init__(self, infile, conv):
        self.title = ""
        self.mol = pybel.Molecule()
        self.data = ""
        self.pharmacophore = ""
        self.valid = False
        self.infile = infile
        self.conv = conv

    def load(self):
        self.valid = False
        if self.infile:
            obmol = pybel.readfile("sdf", self.infile).next()
            self.mol.OBMol = obmol.OBMol
            self.title = obmol.title
            if self.conv.GetData(obmol.OBMol, "PHARMACOPHORE"):
                self.pharmacophore = self.conv.GetData(obmol.OBMol, "PHARMACOPHORE")
            self.valid = True

    def getMol(self):
        return self.mol

    def isValid(self):
        return self.valid
class ReadMCmol:
    def __init__(self, infile):
        self.infile = infile
        self.conv = None
        self.molcnt = 0

    def set_conv(self, conv):
        self.conv = conv

    def load(self):
        if not self.infile:
            return False

        obmol = next(pybel.readfile("sdf", self.infile), None)
        if not obmol:
            return False

        mol = OBBase()
        mol.OBMol = obmol.OBMol
        title = obmol.title

        pharmacophores = []
        for feature in obmol.data:
            if feature.attrib == "PHARMACOPHORE":
                pharmacophores.append(feature.value)

        if pharmacophores:
            sddata = OBVecData()
            sddata.SetAttribute("pharmacophores")
            sddata.SetValue(pharmacophores)
            mol.SetData(sddata)

        self.molcnt += 1
        return True

    def molsRead(self):
        return self.molcnt