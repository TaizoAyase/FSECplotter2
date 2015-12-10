#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FSECplotter.core.logfile import *
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


class HitachiLogfileTestCase(TestCase):
    def setUp(self):
        self.testfile = "./test/fixture/hitachi/00000001.rw1"
        factory = LogfileFactory()
        self.log = factory.create(self.testfile)

    def tearDown(self):
        pass
        
    def test_loaded_filename(self):
        eq_(self.log.filename, '00000001')

    def test_loaded_samplename(self):
        eq_(self.log.sample_name, 'A2a')

    def test_flowrate_is_none(self):
        ok_(self.log.flowrate == 1.0)

    def test_num_detector_is_none(self):
        ok_(self.log.num_detectors is None)

    def test_num_channels_is_none(self):
        ok_(self.log.num_channels is None)

    def test_return_data(self):
        import numpy
        d = self.log.data(**{})
        eq_(type(d), numpy.ndarray)  
