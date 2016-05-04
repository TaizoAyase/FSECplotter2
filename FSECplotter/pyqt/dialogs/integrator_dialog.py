#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.dialogs.ui_integrator_dialog import Ui_IntegratorDialog

class IntegratorDialog(QtWidgets.QDialog):

    def __init__(self, filenames, parent=None):
        super().__init__(parent)
        self.ui = Ui_IntegratorDialog()
        self.ui.setupUi(self)

        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit.setValidator(valid)
        self.ui.lineEdit_2.setValidator(valid)

    def accept(self):
        if not self.ui.lineEdit.text():
            return
        super().accept()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = IntegratorDialog()
    win.show()
    sys.exit(app.exec_())