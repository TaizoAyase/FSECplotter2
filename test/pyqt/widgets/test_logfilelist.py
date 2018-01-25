#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from glob import glob
from unittest import TestCase
from nose.tools import ok_, eq_, raises, nottest

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from FSECplotter import *
from FSECplotter.pyqt.widgets.logfilelist import LogfileListWidget


testfiles = glob('./test/fixture/shimadzu/test*.txt')

app = QtWidgets.QApplication(sys.argv)

class LogfileListWidgetTestCase(TestCase):

    def setUp(self):
        self.form = LogfileListWidget()

    def reset_form_empty(self):
        self.form.delete_all_files()

    def open_file(self, fname):
        self.form.model.add_item(fname)

    def open_files(self):
        for f in testfiles:
            self.open_file(f)

    def test_add_files(self):
        self.reset_form_empty()
        self.open_files()

        eq_(self.form.model.rowCount(), len(testfiles))

    def test_change_all_detector(self):
        self.reset_form_empty()
        self.open_files()

        self.form.setall_detector_comboBox.setCurrentText("A")
        self.form.change_all_detector()

        for i in range(len(testfiles)):
            eq_(self.form.model.item(i, 3).text(), "A")

        self.form.setall_detector_comboBox.setCurrentText("B")
        self.form.change_all_detector()

        for i in range(len(testfiles)):
            eq_(self.form.model.item(i, 3).text(), "B")

    def test_change_all_channel(self):
        self.reset_form_empty()
        self.open_files()

        self.form.setall_channel_comboBox.setCurrentText("1")
        self.form.change_all_channel()

        for i in range(len(testfiles)):
            eq_(self.form.model.item(i, 4).text(), "1")

        self.form.setall_channel_comboBox.setCurrentText("2")
        self.form.change_all_channel()

        for i in range(len(testfiles)):
            eq_(self.form.model.item(i, 4).text(), "2")



    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
