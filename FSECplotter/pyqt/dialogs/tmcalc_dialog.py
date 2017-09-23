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

import re
import os

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from FSECplotter.pyqt.dialogs import Ui_TmCalcDialog
from FSECplotter import calc_yscale_factor, get_enabled_filename
from FSECplotter.pyqt.dialogs import *

class TmCalcDialog(QtWidgets.QDialog):

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.ui = Ui_TmCalcDialog()
        self.ui.setupUi(self)

        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit.setValidator(valid)
        self.ui.lineEdit_2.setValidator(valid)
        self.ui.lineEdit_temp.setValidator(valid)

        self.filenames = get_enabled_filename(self.model)
        for f in self.filenames:
            # self.ui.comboBox.addItem(f)
            temp = self.guess_temperature_from(f,
                self.ui.removeFileExtensionCheckBox.isChecked())
            item = QtWidgets.QTreeWidgetItem([f, temp], 0)
            self.ui.treeWidget.addTopLevelItem(item)

        # signal slot connection
        self.ui.set_temp_button.clicked.connect(self.set_temperature)
        self.ui.updateListButton.clicked.connect(self.update_filelist)

    def set_temperature(self):
        item = self.ui.treeWidget.selectedItems()[0]
        temp = self.ui.lineEdit_temp.text()
        item.setData(1, 0, temp)

    def get_temperature(self):
        n = self.ui.treeWidget.topLevelItemCount()
        list_ = []
        for i in range(n):
            temp = self.ui.treeWidget.topLevelItem(i).data(1, 0)
            list_.append(float(temp))

        return list_

    def update_filelist(self):
        n = len(self.filenames)

        for i in range(n):
            item = self.ui.treeWidget.topLevelItem(i)
            f = self.filenames[i]
            temp = self.guess_temperature_from(f,
                self.ui.removeFileExtensionCheckBox.isChecked())
            item.setData(1, 0, temp)

    def accept(self):
        # not accept when text box(es) are empty
        if not (self.ui.lineEdit.text() and self.ui.lineEdit_2.text()):
            QtWidgets.QApplication.beep()
            return

        min_volume = float(self.ui.lineEdit.text())
        max_volume = float(self.ui.lineEdit_2.text())
        if min_volume >= max_volume:
            QtWidgets.QApplication.beep()
            return

        temp_list = np.array(self.get_temperature())
        scale_factor = calc_yscale_factor(self.model, min_volume, max_volume)

        tmplot_dialog = TmFitDialog(self.model, self)
        try:
            tmplot_dialog.fit(temp_list, scale_factor)
        except RuntimeError as e:
            return
        tmplot_dialog.exec_()
        super().accept()

    # private

    def guess_temperature_from(self, filename, rm_num=True):
        # remove file extensions
        basename = os.path.splitext(filename)[0]

        # remove the last number if removeFileExtensionCheckBox is checked
        if rm_num:
            basename = re.sub(r'_\d+$', '', basename)

        # find all int/float numbers from the given file name
        matched = re.findall(r'\d+\.?\d*', basename)

        if not matched:
            return ""

        selected = [temp for temp in matched if len(temp) <= 2]
        return selected[-1]

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = TmCalcDialog()
    win.show()
    sys.exit(app.exec_())