#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FSECplotter.core.logfile import *
from unittest import TestCase
from nose.tools import ok_, eq_, raises

class LogFileTestCase(TestCase):
    def setUp(self):
        self.testfile = "./test/fixture/test_1.txt"
        self.log = LogFile()
        self.log.parse(self.testfile)

    def tearDown(self):
        pass

    def test_load_file(self):
        eq_(self.log.file_name, "test_1")
        ok_(self.log.sections is not None)

    def test_fine_section(self):
        sec = self.log.find_section("Sample Information")
        eq_(sec.name(), "[Sample Information]")

    def test_flowrate(self):
        eq_(self.log.flowrate, 0.5)

    def test_num_detectors(self):
        eq_(self.log.num_detectors(), 2)

    def test_num_channels(self):
        eq_(self.log.num_channels(), 2)

