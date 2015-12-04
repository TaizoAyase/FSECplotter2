#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.centralWidget = QtWidgets.QWidget(self)
        self.splitter = QtWidgets.QSplitter(self)

        # set list view and plot widgets
        self.treeview = LogfileListWidget(self)
        self.plotarea = PlotArea(self.treeview.model, self)

        #self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        #self.horizontalLayout.addWidget(self.treeview)
        #self.horizontalLayout.addWidget(self.plotarea)

        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.plotarea)

        #self.setCentralWidget(self.centralWidget)
        self.setCentralWidget(self.splitter)

        self.resize(1200, 600)
        self.setWindowTitle("FSEC plotter 2")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
