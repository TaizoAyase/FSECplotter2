#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
