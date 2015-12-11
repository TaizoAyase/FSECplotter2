#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.dialogs.ui_yscale_dialog import Ui_YaxisScalingDialog
#from ui_yscale_dialog import Ui_YaxisScalingDialog

class YaxisScaleDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.ui = Ui_YaxisScalingDialog()
        self.ui.setupUi(self)

        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit.setValidator(valid)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = YaxisScaleDialog()
    win.show()
    sys.exit(app.exec_())