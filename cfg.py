# =============================================================================
# Author: Madhu
#
# Date: Apr 22, 2020
#
# License: BSD 3-Clause
# =============================================================================

# pylint: disable=invalid-name

"""
Configuration file. Change only the following:
    __version__
    __doc__
    MODULE
"""

import sys
import os
import socket
import re

__version__ = "0.0.0"
__doc__ = "ARIMA model"
module = "ARIMA_model"

# Set module path
path = os.path.abspath(os.path.dirname(sys.argv[0]))
path = re.sub(r"(.+)(\/" + module + ".*)", r"\1", path)
path = path + "/"
