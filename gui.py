#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from FSECplotter.pyqt.mainwindow import MainWindow

### main ###
import sys
app = QtWidgets.QApplication(sys.argv)

win = MainWindow()
win.show()

app.exec_()
