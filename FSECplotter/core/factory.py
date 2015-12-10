#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FSECplotter.core.shimadzu import *
from FSECplotter.core.hitachi import *

class LogfileFactory():

    def create(self, filename):
        with open(filename, 'rb') as f:
            if f.read(12) == b"\x0b\x00D2000Chrom":
                return HitachiLogFile(filename)
            else:
                return ShimadzuLogFile(filename)
