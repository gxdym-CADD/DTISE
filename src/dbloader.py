# Pharmit
# Copyright (c) David Ryan Koes, University of Pittsburgh and contributors.
# All rights reserved.

# Pharmit is licensed under both the BSD 3-clause license and the GNU
# Public License version 2. Any use of the code that retains its reliance
# on the GPL-licensed OpenBabel library is subject to the terms of the GPL2.

# Use of the Pharmit code independently of OpenBabel (or any other
# GPL2 licensed software) may choose between the BSD or GPL licenses.

# See the LICENSE file provided with the distribution for more information.

import os
from typing import List, Dict

class StripedSearchers:
    pass  # Placeholder for StripedSearchers class

def loadDatabases(dbpaths: List[str], databases: 'StripedSearchers'):
    # fill in databases present in dbpaths
    pass

def loadFromPrefixes(prefixes: List[str], databases: Dict[str, 'StripedSearchers']):
    # populated databases using prefixes
    pass

def loadNewFromPrefixes(prefixes: List[str], databases: Dict[str, 'StripedSearchers'], olddatabases: Dict[str, 'StripedSearchers'], deactivate: bool = False):
    # populate new databases using prefixes and compare with old databases
    pass