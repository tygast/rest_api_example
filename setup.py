# -*- coding: utf-8 -*-
"""Run Setup Script to build collections in the maintenance program"""
import re

from setuptools import setup

with open("src/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    version=version,
    description=("A program used to assit inventory and maintenance management"),
)
