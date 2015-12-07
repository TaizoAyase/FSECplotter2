#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs

from FSECplotter.core.section import *
from unittest import TestCase
from nose.tools import ok_, eq_, raises

class SectionTestCase(TestCase):
    def setUp(self):
        self.header = "[LC Chromatogram(Detector A-Ch1)]\n"
        self.param_line = "End Time(min)\t60.000\n"
        self.data_line = "0.01667\t4\n"

    def tearDown(self):
        pass

    def test_init(self):
        sec = Section(self.header)
        eq_(sec.name(), "[LC Chromatogram(Detector A-Ch1)]")

    def test_add_param(self):
        sec = Section(self.header)
        sec.append_data(self.param_line)
        eq_(sec.params()[0][0], "End Time(min)")
        eq_(sec.params()[0][1], "60.000")

    def test_add_data_not_converted_to_numpy(self):
        sec = Section(self.header)
        sec.append_data(self.data_line)
        eq_(sec.data()[0][0], 0.01667)
        eq_(sec.data()[0][0], 4)

    def test_add_data(self):
        sec = Section(self.header)
        sec.append_data(self.data_line)
        sec.convert_to_npary()
        eq_(sec.data()[0][0], 0.01667)
        eq_(sec.data()[0][1], 4)

    def test_add_data_access_to_param(self):
        sec = Section(self.header)
        sec.append_data(self.data_line)
        sec.convert_to_npary()
        eq_(len(sec.params()), 0)

    def test_add_param_access_to_data(self):
        sec = Section(self.header)
        sec.append_data(self.param_line)
        eq_(len(sec.data()), 0)
