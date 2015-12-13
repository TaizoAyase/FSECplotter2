#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.dialogs.ui_tmcalc_dialog import Ui_TmCalcDialog
import re

class TmCalcDialog(QtWidgets.QDialog):

    def __init__(self, filenames, parent=None):
        super().__init__(parent)
        self.ui = Ui_TmCalcDialog()
        self.ui.setupUi(self)

        valid = QtGui.QDoubleValidator()
        self.ui.lineEdit.setValidator(valid)
        self.ui.lineEdit_temp.setValidator(valid)

        self.ui.treeWidget.setHeaderLabels(["Filename", "Temperature"])

        for f in filenames:
            self.ui.comboBox.addItem(f)
            temp = self.__guess_temp(f)
            item = QtWidgets.QTreeWidgetItem([f, temp], 0)
            self.ui.treeWidget.addTopLevelItem(item)

        self.ui.treeWidget.setColumnWidth(0, 150)
        self.ui.treeWidget.setColumnWidth(1, 100)

        self.ui.set_temp_button.clicked.connect(self.set_temperature)

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

    def accept(self):
        if not self.ui.lineEdit.text():
            return
        super().accept()

    # private

    def __guess_temp(self, f):
        m = re.findall('\d+\.?\d*', f)

        # if m is empty,
        if not m:
            return ""

        selected = [temp for temp in m if len(temp) <= 2]
        return selected[-1]

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = TmCalcDialog()
    win.show()
    sys.exit(app.exec_())