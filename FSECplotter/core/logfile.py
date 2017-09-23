#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2017, TaizoAyase, tikuta, biochem-fan

This file is part of FSECplotter2.

FSECplotter2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import print_function
from abc import ABCMeta, abstractmethod
import os


class Logfile(metaclass=ABCMeta):
    """Abstract class for various logfiles"""
    def __init__(self, filename):
        self.flowrate = 1.0
        self.num_detectors = None
        self.num_channels = None

        # parse
        self.filename, ext = os.path.splitext(os.path.basename(filename))
        self._parse(filename)

    @abstractmethod
    def data(self, **kwargs):
        pass

    @abstractmethod
    def _parse(self, filename):
        pass


# base class for Exception classes for logfiles
class LogfileError(Exception):
    pass
