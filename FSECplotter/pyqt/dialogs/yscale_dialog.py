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

from PyQt5 import QtCore, QtGui, QtWidgets

from FSECplotter.pyqt.dialogs import Ui_YaxisScalingDialog

class YaxisScaleDialog(QtWidgets.QDialog):

    def __init__(self, filenames, parent=None):
        super().__init__(parent)
        self.ui = Ui_YaxisScalingDialog()
        self.ui.setupUi(self)

        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit.setValidator(valid)
        self.ui.lineEdit_2.setValidator(valid)

        #for f in filenames:
            #self.ui.filename_for_normal.addItem(f)

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

        super().accept()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = YaxisScaleDialog()
    win.show()
    sys.exit(app.exec_())