#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from unittest import TestCase
from nose.tools import ok_, eq_, raises

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from FSECplotter import *
from FSECplotter.pyqt.models import LogfileModel
from FSECplotter.pyqt.dialogs import *


testfiles = ['./test/fixture/shimadzu/test_1.txt',
    './test/fixture/shimadzu/test_2.txt',
    './test/fixture/shimadzu/test_3.txt']
MAX_VOLUME = [15.141665, 15.229165, 15.254165]
MAX_VALUE = [676124.0, 304409.0, 319399.0]

app = QtWidgets.QApplication(sys.argv)

class PeakTableDialogTestCase(TestCase):

    def setUp(self):
        self.model = LogfileModel(0, 6, None)
        for f in testfiles:
            self.model.add_item(f)

        # select Detector B and channel 2
        self.model.item(0, 3).setText("B")
        self.model.item(0, 4).setText("2")

        self.form = PeakTableDialog(self.model)

    def reset_form_empty(self):
        self.form.ui.lineEdit_min.setText("")
        self.form.ui.lineEdit_max.setText("")

    def test_defaults(self):
        # no text is set in default
        eq_(self.form.ui.lineEdit_min.text(), "")
        eq_(self.form.ui.lineEdit_max.text(), "")

        # normalization check box is not checked
        eq_(self.form.ui.normalizeCheckBox.checkState(), 0)

        # no item is set in default
        eq_(self.form.ui.tableWidget.rowCount(), 1)
        eq_(self.form.ui.tableWidget.item(0, 0), None)
        eq_(self.form.ui.tableWidget.item(0, 1), None)
        eq_(self.form.ui.tableWidget.item(0, 2), None)

    def test_peak_search(self):
        self.reset_form_empty()

        self.form.ui.lineEdit_min.setText("0.0")
        self.form.ui.lineEdit_max.setText("30.0")

        QTest.mouseClick(self.form.ui.updateButton, Qt.LeftButton)

        eq_(self.form.ui.tableWidget.rowCount(), len(testfiles))

        filename, _ = os.path.splitext(os.path.basename(testfiles[0]))
        eq_(self.form.ui.tableWidget.item(0, 0).text(), filename)
        eq_(self.form.ui.tableWidget.item(0, 1).text(), str(MAX_VOLUME[0]))
        eq_(self.form.ui.tableWidget.item(0, 2).text(), str(MAX_VALUE[0]))

    def test_automated_update(self):
        self.reset_form_empty()

        self.form.ui.lineEdit_min.setText("0.0")
        self.form.ui.lineEdit_max.setText("30.0")

        eq_(self.form.ui.tableWidget.rowCount(), len(testfiles))

        filename, _ = os.path.splitext(os.path.basename(testfiles[0]))
        eq_(self.form.ui.tableWidget.item(0, 0).text(), filename)
        eq_(self.form.ui.tableWidget.item(0, 1).text(), str(MAX_VOLUME[0]))
        eq_(self.form.ui.tableWidget.item(0, 2).text(), str(MAX_VALUE[0]))

    def test_peak_normalization(self):
        self.reset_form_empty()

        self.form.ui.lineEdit_min.setText("0.0")
        self.form.ui.lineEdit_max.setText("30.0")

        self.form.ui.normalizeCheckBox.setCheckState(2)

        QTest.mouseClick(self.form.ui.updateButton, Qt.LeftButton)

        eq_(self.form.ui.tableWidget.rowCount(), len(testfiles))

        filename, _ = os.path.splitext(os.path.basename(testfiles[0]))
        eq_(self.form.ui.tableWidget.item(0, 0).text(), filename)
        eq_(self.form.ui.tableWidget.item(0, 1).text(), str(MAX_VOLUME[0]))
        eq_(self.form.ui.tableWidget.item(0, 2).text(), "1.0")

    def tearDown(self):
        del self.form


if __name__ == "__main__":
    unittest.main()
