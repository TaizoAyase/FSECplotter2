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


testfiles = glob('./test/fixture/shimadzu/FSEC-TS_tests/*.txt')

app = QtWidgets.QApplication(sys.argv)

class TmCalcDialogTestCase(TestCase):

    def setUp(self):
        self.model = LogfileModel(0, 6, None)

        for i, f in enumerate(testfiles):
            self.model.add_item(f)

            # select Detector A and channel 1
            self.model.item(i, 3).setText("B")
            self.model.item(i, 4).setText("1")

        self.form = TmCalcDialog(self.model)

    def reset_form_empty(self):
        self.form.ui.removeFileExtensionCheckBox.setCheckState(0)
        self.form.ui.lineEdit_temp.setText("")
        self.form.ui.lineEdit.setText("")
        self.form.ui.lineEdit_2.setText("")

        self.form.tmplot_dialog.fig_saved = False
        self.form.tmplot_dialog.fit_complete = False

    def test_defaults(self):
        eq_(self.form.ui.lineEdit_temp.text(), "")
        eq_(self.form.ui.lineEdit.text(), "")
        eq_(self.form.ui.lineEdit_2.text(), "")

    def test_parse_temperature(self):
        self.reset_form_empty()

        self.form.ui.removeFileExtensionCheckBox.setCheckState(0)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        top_item = self.form.ui.treeWidget.topLevelItem(0)
        eq_(top_item.data(1, 0), "17")

    def test_parse_temperature2(self):
        self.reset_form_empty()

        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        top_item = self.form.ui.treeWidget.topLevelItem(0)
        eq_(top_item.data(1, 0), "4")

    def test_set_temperature(self):
        self.reset_form_empty()

        # set the temperature of first item to "20"
        self.form.ui.lineEdit_temp.setText("20")

        top_item = self.form.ui.treeWidget.topLevelItem(0)
        self.form.ui.treeWidget.setCurrentItem(top_item, 0, 
            QtCore.QItemSelectionModel.Select)
        QTest.mouseClick(self.form.ui.set_temp_button, Qt.LeftButton)

        top_item = self.form.ui.treeWidget.topLevelItem(0)
        eq_(top_item.data(1, 0), "20")

    def test_min_max_volume_inverse(self):
        self.reset_form_empty()
        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        self.form.ui.lineEdit.setText("2")
        self.form.ui.lineEdit_2.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.tmplot_dialog.fit_complete)

    def test_min_volume_empty(self):
        self.reset_form_empty()
        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        self.form.ui.lineEdit_2.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.tmplot_dialog.fit_complete)

    def test_max_volume_empty(self):
        self.reset_form_empty()
        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        self.form.ui.lineEdit.setText("1")

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.tmplot_dialog.fit_complete)

    def test_volume_empty(self):
        self.reset_form_empty()
        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(not self.form.tmplot_dialog.fit_complete)

    def test_accept(self):
        self.reset_form_empty()

        self.form.ui.removeFileExtensionCheckBox.setCheckState(2)
        QTest.mouseClick(self.form.ui.updateListButton, Qt.LeftButton)

        self.form.ui.lineEdit.setText("1")
        self.form.ui.lineEdit_2.setText("2")

        # prevent showing the warning dialog
        self.form.tmplot_dialog.fig_saved = True
        ok_button = self.form.tmplot_dialog.ok_button
        QtCore.QTimer.singleShot(0, ok_button.clicked)
        # close the child dialog
        okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

        ok_(self.form.tmplot_dialog.fit_complete)


if __name__ == "__main__":
    unittest.main()
