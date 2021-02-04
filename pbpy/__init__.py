"""
Primebots.it Python API Wrapper

Wrapper per l'api di primebots.it

:copyright: (c) 2021 Giuseppe Pollio & primebots.it

:license: MIT, see LICENSE for more details.
"""

__title__ = 'primebotspy'
__author__ = "Giuseppe 'Polliog' Pollio"
__license__ = 'MIT'
__version__ = '1.0'

from collections import namedtuple

from .client import PBclient

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=4, micro=0, releaselevel='final', serial=0)