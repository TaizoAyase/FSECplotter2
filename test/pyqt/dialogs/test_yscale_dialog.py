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


testfiles = glob('./test/fixture/shimadzu/test*.txt')

app = QtWidgets.QApplication(sys.argv)

class YaxisScaleDialogTestCase(TestCase):

    def setUp(self):
        self.form = YaxisScaleDialog()

    def reset_form_empty(self):
        self.form.ui.lineEdit.setText("")
        self.form.ui.lineEdit_2.setText("")
        self.form.scale_accepted = False

    def test_defaults(self):
        eq_(self.form.ui.lineEdit.text(), "")
        eq_(self.form.ui.lineEdit_2.text(), "")

    def test_min_max_volume_inverse(self):
        self.reset_form_empty()
        self.form.ui.lineEdit.setText("2")
        self.form.ui.lineEdit_2.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.scale_accepted)

    def test_min_volume_empty(self):
        self.reset_form_empty()
        self.form.ui.lineEdit_2.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.scale_accepted)

    def test_max_volume_empty(self):
        self.reset_form_empty()
        self.form.ui.lineEdit.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.scale_accepted)

    def test_volume_empty(self):
        self.reset_form_empty()

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.scale_accepted)

    def test_accept(self):
        self.reset_form_empty()

        self.form.ui.lineEdit.setText("0")
        self.form.ui.lineEdit_2.setText("30")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(self.form.scale_accepted)
        eq_(self.form.min_volume, 0)
        eq_(self.form.max_volume, 30)

    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
