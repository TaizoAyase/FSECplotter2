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

from FSECplotter.pyqt.dialogs import *
from FSECplotter.pyqt.mainwindow import APP_VERSION


app = QtWidgets.QApplication(sys.argv)

class FSECplotterUtilsTestCase(TestCase):

    def setUp(self):
        self.form = AboutDialog()

    def test_version_number(self):
        ok_(APP_VERSION in self.form.ui.labelVersion.text())

    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
