#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np


class Section:
    # initialized with section header name

    def __init__(self, header_str):
        self.__section_name = header_str.strip("\r\n")
        self.__parameters = []
        #self.__data_table = np.array([[0, 0]])
        self.__data_table = []
        self.__np_data_table = None

    # add row to the datatable
    # list should be a array of float
    def append_data(self, line):
        ary = line.strip("\r\n").split("\t")

        # try to convert the first col to float
        try:
            float(ary[0])
        # if cannot, this is the paramter part
        except ValueError:
            self.__parameters.append(ary)
            return self

        # if can, this is the time table part
        ary_f = [float(ary[0]), float(ary[1])]
        #tmp = np.r_[self.__data_table, [[ary_f[0], ary_f[1]]]]
        #self.__data_table = tmp
        self.__data_table.append([ary_f[0], ary_f[1]])
        return self

    def convert_to_npary(self):
        self.__np_data_table = np.array(self.__data_table)

    # getters
    def name(self):
        return self.__section_name

    def data(self):
        if self.__np_data_table.any():
            return self.__np_data_table
        return self.__data_table

    def params(self):
        return self.__parameters
