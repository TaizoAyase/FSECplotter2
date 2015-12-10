#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FSECplotter.core.factory import *
from FSECplotter.core.shimadzu import Section
from unittest import TestCase
from nose.tools import ok_, eq_, raises


class ShimazuLogFileTestCase(TestCase):
    def setUp(self):
        self.testfile = "./test/fixture/shimadzu/test_1.txt"
        factory = LogfileFactory()
        self.log = factory.create(self.testfile)

    def tearDown(self):
        pass

    def test_loaded_filename(self):
        eq_(self.log.filename, "test_1")

    def test_has_section(self):
        ok_(self.log.sections is not None)

    def test_flowrate(self):
        eq_(self.log.flowrate, 0.5)

    def test_num_detectors(self):
        eq_(self.log.num_detectors, 2)

    def test_num_channels(self):
        eq_(self.log.num_channels, 2)

    def test_return_data(self):
        import numpy
        d = self.log.data(**{'detector':'B', 'channel':2})
        eq_(type(d), numpy.ndarray)

    @raises(NoSectionError)
    def test_nonexisting_section_access(self):
        self.log.data(**{'detector':'B', 'channel':3})


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
        ok_(sec.data() is None)

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
        ok_(sec.data() is None)
