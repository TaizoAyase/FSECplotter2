#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from FSECplotter.core.logfile import Logfile

import numpy as np


class HitachiLogFile(Logfile):

    def __init__(self, filename):
        self.sample_name = None
        super().__init__(filename)

    def data(self, **param):
        # param is not used
        return self.__data

    def _parse(self, filename):
        f = open(filename, 'rb')
        #if f.read(12) == b"\x0b\x00D2000Chrom":
            #return self.__parse_logfile_hitachi(f)

        SamplingPeriod = 400  # msec
        RFUConversionFactor = 0.00025

        self.flowrate = 1.0

        f.seek(0)
        data = f.read()
        f.close()

        pos = data.index(b"VialName") + len(b"VialName") + 5
        length = data[pos] - 1  # I'm not sure if this will exceed FF
        self.sample_name = data[(pos + 2):(pos + 2 + length)].decode("ascii")

        pos = data.index(b"Boundary")
        pos += len(b"Boundary") + 7  # "Boundary" 00 06 00 00 00 00
        data = data[pos:-1]

        data_table = []

        i = 0
        while (i + 2 < len(data)):
            val = (data[i] << 16) + (data[i + 1] << 8) + data[i + 2]
            if val > 200 * 256 * 256:
                val = 0  # AD HOC: actually this is SIGNED

            time = i / 3 * SamplingPeriod / 1000.0 / 60.0
            intensity = val * RFUConversionFactor
            data_table.append([time, intensity])
            i += 3

        self.__data = np.array(data_table)
