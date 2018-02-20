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
from FSECplotter.pyqt.mainwindow import MainWindow


testfiles = glob('./test/fixture/shimadzu/test*.txt')

app = QtWidgets.QApplication(sys.argv)

class MainWindowTestCase(TestCase):

    def setUp(self):
        self.form = MainWindow()

    def test_startup(self):
        ok_(True)

    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
