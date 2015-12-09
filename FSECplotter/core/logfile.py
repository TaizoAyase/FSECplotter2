#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import codecs
import re
import os
from .section import Section


class LogFile:

    def __init__(self):
        self.sections = []
        self.file_name = None  # file basename without extension
        self.flowrate = None
        self.num_detectors = None
        self.num_channels = None

    def parse(self, filename):
        self.file_name, ext = os.path.splitext(os.path.basename(filename))

        self.__parse_logfile(filename)
        # remove extension from file basename
        self.__set_flowrate()
        self.__set_num_detectors()
        self.__set_num_channels()
        return self

    def append_section(self, section):
        section.convert_to_npary()
        self.sections.append(section)
        return self.sections

    # return section that match the RE of section_name
    def find_section(self, section_name):
        # first, replace "()" to "\(\)"
        secname = self.__sub_parenthesis(section_name)
        pat = re.compile(secname)
        name_ary = [x.name() for x in self.sections]
        index = [i for i, name in enumerate(name_ary) if pat.search(name)]
        if not index:
            raise NoSectionError
        return self.sections[index[0]]

    # private methods

    # get flow rate from the file name of method file
    # if cannot, raise Error
    def __set_flowrate(self):
        methodfiles_ary = self.__get_params_ary(
            "Original Files", "Method File")

        # search float in file name
        pat = re.compile(r"\d\.\d+")
        matched_str = pat.findall(methodfiles_ary[0])
        if matched_str:
            self.flowrate = float(matched_str[0])
        else:
            raise NoMatchedFlowRateError

    # detector/channel num. is written in Configuration section
    def __set_num_detectors(self):
        num_detectors_ary = self.__get_params_ary(
            "Configuration", "# of Detectors")
        self.num_detectors = int(num_detectors_ary[0])
        return self.num_detectors

    def __set_num_channels(self):
        num_channels_ary = self.__get_params_ary(
            "Configuration", "# of Channels")
        self.num_channels = int(num_channels_ary[-1])
        return self.num_channels

    def __parse_logfile_hitachi(self, f):
        SamplingPeriod = 400 # msec
        RFUConversionFactor =0.00025

        self.__flow_rate = 0.8

        f.seek(0)
        data = f.read()
        pos = data.index(b"VialName") + len(b"VialName") + 5
        length = data[pos] - 1 # I'm not sure if this will exceed FF
        self.file_name = data[(pos + 2):(pos + 2 + length)].decode("ascii")

        pos = data.index(b"Boundary")
        pos += len(b"Boundary") + 7 # "Boundary" 00 06 00 00 00 00
        data = data[pos:-1]

        sec = Section("LC Chromatogram(Detector A-Ch1)") # FIXME

        i = 0
        while (i + 2 < len(data)):
            val = (data[i] << 16) + (data[i + 1] << 8) + data[i + 2]
            if val > 200 * 256 * 256:
                val = 0 # AD HOC: actually this is SIGNED

            sec.append_data("%f\t%f" % (i / 3 * SamplingPeriod / 1000.0 / 60.0, 
                                        val * RFUConversionFactor))
            i += 3

        self.append_section(sec)

    def __parse_logfile(self, f_path):
        header_pattern = re.compile(r"\[.+\]")

        with open(f_path, "rb") as f:
            if f.read(12) == b"\x0b\x00D2000Chrom":
                return self.__parse_logfile_hitachi(f)

        header_flag = False
        with codecs.open(f_path, "r", "shift_jis") as f:
            for line in f:
                # search the header line
                if re.match(header_pattern, line):
                    sec = Section(line)
                    header_flag = True

                # search the end of the section
                if re.match(r"^\s+$", line):
                    if header_flag:
                        header_flag = False
                        self.append_section(sec)
                        del sec

                sec.append_data(line) if 'sec' in locals() else None

    def __sub_parenthesis(self, section_name):
        tmp = re.sub(r"\(", "\(", section_name)
        return re.sub(r"\)", "\)", tmp)

    def __get_params_ary(self, section_name, param_name):
        params_ary = self.find_section(section_name).params()
        for par in params_ary:
            if param_name in par:
                tmp_name_ary = par.copy() # deep copy of list
                tmp_name_ary.pop(0) # remove param name
                return tmp_name_ary


# exception
class NoMatchedFlowRateError(Exception):
    pass


class NoSectionError(Exception):
    pass
