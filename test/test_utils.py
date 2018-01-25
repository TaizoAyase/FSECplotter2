#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from glob import glob
from unittest import TestCase
from nose.tools import ok_, eq_, raises

import numpy.testing as npt

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from FSECplotter import *
from FSECplotter.pyqt.models import LogfileModel
from FSECplotter.pyqt.dialogs import *


testfiles = glob('./test/fixture/shimadzu/test*.txt')

SCALE_FACTOR = [1.0, 0.45022659, 0.47239708]
INTEGRATED_PEAK = [994047.56563499896, 548488.86240500025, 712461.85801999958]
MAX_DECIMAL = 5
MAX_VOLUME = 15.141665
MAX_VALUE = 676124.0

app = QtWidgets.QApplication(sys.argv)

class FSECplotterUtilsTestCase(TestCase):

    def setUp(self):
        self.model = LogfileModel(0, 6, None)

        for i, f in enumerate(testfiles):
            self.model.add_item(f)
            # select Detector A and channel 1
            self.model.item(i, 3).setText("B")
            self.model.item(i, 4).setText("2")

    def test_calc_yscale_factor(self):
        scale_factor = calc_yscale_factor(self.model, 0, 30)
        npt.assert_almost_equal(scale_factor, SCALE_FACTOR,
            decimal=MAX_DECIMAL)

    def test_find_peak(self):
        filenames, peak_x, peak_y = calc_max_peak(self.model, 0, 30)

        fname_true = [os.path.splitext(os.path.basename(f))[0] for f in testfiles]
        eq_(filenames, fname_true)
        npt.assert_almost_equal(peak_x[0], MAX_VOLUME,
            decimal=MAX_DECIMAL)
        npt.assert_almost_equal(peak_y[0], MAX_VALUE,
            decimal=MAX_DECIMAL)

    def test_get_enabled_filename(self):
        fname = get_enabled_filename(self.model)
        fname_true = [os.path.splitext(os.path.basename(f))[0] for f in testfiles]
        eq_(fname, fname_true)

        self.model.item(1, 0).setCheckState(0)
        fname = get_enabled_filename(self.model)
        del fname_true[1]
        eq_(fname, fname_true)

        self.model.item(1, 0).setCheckState(2)

    def test_peak_integrate(self):
        integrated = peak_integrate(self.model, 0, 30)
        npt.assert_almost_equal(integrated, INTEGRATED_PEAK,
            decimal=MAX_DECIMAL)

    def tearDown(self):
        del self.model


if __name__ == "__main__":
    unittest.main()
