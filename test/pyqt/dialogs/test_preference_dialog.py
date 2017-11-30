#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from glob import glob
from unittest import TestCase
from nose.tools import ok_, eq_, raises

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from FSECplotter import *
from FSECplotter.pyqt.models import LogfileModel
from FSECplotter.pyqt.dialogs import *
from FSECplotter.pyqt.mainwindow import DEFAULTS


testfiles = glob('./test/fixture/shimadzu/test*.txt')

app = QtWidgets.QApplication(sys.argv)

class PreferenceDialogTestCase(TestCase):

    def setUp(self):
        self.form = PreferenceDialog(DEFAULTS)
        self.ui = self.form.ui

    def reset_form(self):
        self.tearDown()
        self.setUp()

    def test_defaults(self):
        self.reset_form()

        eq_(self.ui.detector_comboBox.currentIndex(), DEFAULTS['detector'])
        eq_(self.ui.channel_spinBox.value(), DEFAULTS['channel'])
        eq_(self.ui.flowrate_spinBox.value(), DEFAULTS['flowrate'])
        eq_(self.ui.linewidth_spinBox.value(), DEFAULTS['linewidth'])
        eq_(float(self.ui.x_min_lineEdit.text()), DEFAULTS['x_min'])
        eq_(float(self.ui.x_max_lineEdit.text()), DEFAULTS['x_max'])
        eq_(self.ui.x_axis_comboBox.currentIndex(), DEFAULTS['x_axis'])
        eq_(float(self.ui.ts_gain_lineEdit.text()), DEFAULTS['ts_gain'])
        eq_(float(self.ui.ts_tm_lineEdit.text()), DEFAULTS['ts_tm'])
        eq_(float(self.ui.figure_dpi_lineEdit.text()), DEFAULTS['figure_dpi'])
        eq_(self.ui.sns_style_comboBox.currentIndex(), DEFAULTS['sns_style'])
        eq_(self.ui.sns_context_comboBox.currentIndex(), DEFAULTS['sns_context'])
        eq_(self.ui.use_seaborn_checkBox.checkState(), DEFAULTS['use_seaborn'])

    def test_change_params_detector(self):
        self.ui.detector_comboBox.setCurrentIndex(0)
        params = self.form.get_params()
        eq_(params['detector'], 0)

        self.ui.detector_comboBox.setCurrentIndex(1)
        params = self.form.get_params()
        eq_(params['detector'], 1)

    def test_change_params_channel(self):
        self.ui.channel_spinBox.setValue(1)
        params = self.form.get_params()
        eq_(params['channel'], 1)

        self.ui.channel_spinBox.setValue(2)
        params = self.form.get_params()
        eq_(params['channel'], 2)

    def test_change_params_flowrate(self):
        self.ui.flowrate_spinBox.setValue(0.5)
        params = self.form.get_params()
        eq_(params['flowrate'], 0.5)

    def test_change_params_x_min_max(self):
        self.ui.x_min_lineEdit.setText("10.0")
        params = self.form.get_params()
        eq_(params['x_min'], "10.0")

        self.ui.x_max_lineEdit.setText("10.0")
        params = self.form.get_params()
        eq_(params['x_max'], "10.0")

    def test_change_params_x_axis(self):
        self.ui.x_axis_comboBox.setCurrentIndex(1)
        params = self.form.get_params()
        eq_(params['x_axis'], 1)

    def test_change_params_ts_gain(self):
        self.ui.ts_gain_lineEdit.setText("10.0")
        params = self.form.get_params()
        eq_(params['ts_gain'], "10.0")

    def test_change_params_ts_tm(self):
        self.ui.ts_tm_lineEdit.setText("10.0")
        params = self.form.get_params()
        eq_(params['ts_tm'], "10.0")

    def test_change_params_figure_dpi(self):
        self.ui.figure_dpi_lineEdit.setText("600")
        params = self.form.get_params()
        eq_(params['figure_dpi'], "600")

    def test_seaborn_checkbox(self):
        # seaborn is off
        self.ui.use_seaborn_checkBox.setCheckState(0)
        ok_(not self.ui.seaborn_style_groupBox.isEnabled())

        # seaborn is on
        self.ui.use_seaborn_checkBox.setCheckState(2)
        ok_(self.ui.seaborn_style_groupBox.isEnabled())

    def test_seaborn_style_context(self):
        self.reset_form()
        self.ui.use_seaborn_checkBox.setCheckState(2)

        self.ui.sns_style_comboBox.setCurrentIndex(1)
        self.ui.sns_context_comboBox.setCurrentIndex(1)

        params = self.form.get_params()
        eq_(params['sns_style'], 1)
        eq_(params['sns_context'], 1)

    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
