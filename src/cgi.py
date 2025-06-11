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
 cgi.py

 Created on: Mar 11, 2010
 Author: dkoes
"""

from typing import Dict, Optional
import fcgi
import cgicc

def cgi_tag_exists(cgi: cgicc.Cgicc, name: str) -> bool:
    return name in cgi.get_list()

def cgi_get_int(cgi: cgicc.Cgicc, name: str) -> int:
    try:
        value = cgi[name]
        return int(value)
    except (ValueError, KeyError):
        return 0

def cgi_get_string(cgi: cgicc.Cgicc, name: str) -> str:
    try:
        return cgi[name]
    except KeyError:
        return ""

def cgi_get_double(cgi: cgicc.Cgicc, name: str) -> float:
    try:
        value = cgi[name]
        return float(value)
    except (ValueError, KeyError):
        return 0.0

def cgi_dump(cgi: cgicc.Cgicc) -> str:
    return str(cgi)

class FastCgiIO(cgicc.CgiInput):
    def __init__(self, request: fcgi.Request):
        self.fRequest = request
        self.fOutBuf = fcgi.OutputStreamBuffer(request.stdout)
        self.fErrBuf = fcgi.OutputStreamBuffer(request.stderr)
        self.fErr = cgicc.CgiOutput(self.fErrBuf)
        self.fEnv = dict(os.environ)

    def read(self, length: int) -> bytes:
        return self.fRequest.stdin.read(length)

    def getenv(self, var_name: str) -> Optional[str]:
        return self.fEnv.get(var_name)

    def err(self) -> cgicc.CgiOutput:
        return self.fErr