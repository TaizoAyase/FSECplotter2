#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2017, TaizoAyase, tikuta, biochem-fan

This file is part of FSECplotter2.

FSECplotter2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from FSECplotter import *
from FSECplotter.pyqt.dialogs import Ui_PeakTableDialog


class PeakTableDialog(QtWidgets.QDialog):

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.default_filename = "peaktable.csv"

        self.ui = Ui_PeakTableDialog()
        self.ui.setupUi(self)

        # set validator
        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit_min.setValidator(valid)
        self.ui.lineEdit_max.setValidator(valid)

        # set table header to stretch mode
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        # signal-slot connection
        self.ui.okButton.clicked.connect(self.accept)
        self.ui.saveCSVButton.clicked.connect(self.saveCSV)
        self.ui.updateButton.clicked.connect(self.update)
        self.ui.lineEdit_min.textChanged.connect(self.update)
        self.ui.lineEdit_max.textChanged.connect(self.update)

    # TODO: implement it
    def saveCSV(self):
        csvfile = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save CSV",
            os.path.expanduser("~") + "/" + self.default_filename,
            filter="Text files (*.csv)")

        if not csvfile[0]:
            return

        text = "Filenames, Volume, Intensity\n"
        for i in range(self.ui.tableWidget.rowCount()):
            text += self.ui.tableWidget.item(i, 0).text()
            text += ", "
            text += self.ui.tableWidget.item(i, 1).text()
            text += ", "
            text += self.ui.tableWidget.item(i, 2).text()
            text += "\n"

        with open(csvfile[0], "w+") as f:
            f.write(text)

    def update(self):
        # not accept when text box(es) are empty
        if not (self.ui.lineEdit_min.text() and self.ui.lineEdit_max.text()):
            QtWidgets.QApplication.beep()
            return

        min_volume = float(self.ui.lineEdit_min.text())
        max_volume = float(self.ui.lineEdit_max.text())
        if min_volume >= max_volume:
            QtWidgets.QApplication.beep()
            return

        self.update_table(min_volume, max_volume)

    def update_table(self, min_vol, max_vol):
        f_ary, max_vol_ary, max_val_ary = calc_max_peak(
            self.model, min_vol, max_vol)

        row = 0
        for f, max_x, max_y in zip(f_ary, max_vol_ary, max_val_ary):
            # set item to table
            item = QtWidgets.QTableWidgetItem(f)
            self.ui.tableWidget.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(str(max_x))
            self.ui.tableWidget.setItem(row, 1, item)
            item = QtWidgets.QTableWidgetItem(str(max_y))
            self.ui.tableWidget.setItem(row, 2, item)

            row += 1

        if self.ui.normalizeCheckBox.checkState() == 2:
            max_val_ary /= np.max(max_val_ary)
            for i in range(self.ui.tableWidget.rowCount()):
                item = QtWidgets.QTableWidgetItem(str(max_val_ary[i]))
                self.ui.tableWidget.setItem(i, 2, item)

    def calc_max_peak(self, data, min_vol, max_vol):
        # set the x-index of min/max value
        minidx = np.argmin(np.abs(data[:, 0] - min_vol))
        maxidx = np.argmin(np.abs(data[:, 0] - max_vol))

        # get max volume and intensity
        max_value = max(data[minidx:maxidx, 1])
        max_volume_idx = np.argmax(data[minidx:maxidx, 1])
        max_volume = data[max_volume_idx, 0] + min_vol
        # alternative implementation
        # max_volume = d[max_volume_idx+minidx, 0]

        return max_volume, max_value


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = PeakTableDialog()
    win.show()
    sys.exit(app.exec_())