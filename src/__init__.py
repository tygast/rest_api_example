# -*- coding: utf-8 -*-
"""A program used to assit inventory and maintenance management"""

__author__ = "User 1"
__license__ = "proprietary"
__copyright__ = "*******"

__version__ = "0.0.1"

__maintainer__ = "User 1"

from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("DEBUG"))
