#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.centralWidget = QtWidgets.QWidget(self)

        # set list view and plot widgets
        self.treeview = LogfileListWidget(self)
        self.plotarea = PlotArea(self.treeview.model, self)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.addWidget(self.treeview)
        self.horizontalLayout.addWidget(self.plotarea)

        self.setCentralWidget(self.centralWidget)

        self.resize(1200, 600)
        self.setWindowTitle("FSEC plotter 2")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
