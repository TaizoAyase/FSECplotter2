#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FSECplotter.core.factory import *
from unittest import TestCase
from nose.tools import ok_, eq_, raises


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
