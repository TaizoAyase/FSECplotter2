#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from .logfilelist import *
from .plotwidget import *

from glob import glob

TEST_FILES = glob("./test/fixture/test*.txt")


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent = None):
    super(MainWindow, self).__init__(parent)
    #layout = QtWidgets.QVBoxLayout(self)
    self.centralWidget = QtWidgets.QWidget(self)

    # set list view and plot widgets
    self.treeview = LogfileListWidget(self.centralWidget)
    self.plotarea = PlotArea(self.centralWidget)   

    # make first plot
    data = self.treeview.model.get_current_data()
    self.plotarea.plot_fig(data)

    # set buttons
    self.redraw_button = QtWidgets.QPushButton(self.centralWidget)
    self.redraw_button.setObjectName("Redraw button")
    self.redraw_button.setText("Redraw")

    self.savefig_button = QtWidgets.QPushButton(self.centralWidget)
    self.savefig_button.setObjectName("Save Fig. button")
    self.savefig_button.setText("Save Fig.")

    # signal slot definition
    #self.redraw_button.clicked.connect(self.redraw)
    #self.savefig_button.clicked.connect(self.save_figure)

    # right-hand layout
    self.gridLay2 = QtWidgets.QGridLayout()
    self.gridLay2.addWidget(self.redraw_button, 0, 0, 1, 1)
    self.gridLay2.addWidget(self.savefig_button, 0, 1, 1, 1)

    self.verLay2 = QtWidgets.QVBoxLayout()
    self.verLay2.addWidget(self.plotarea)
    self.verLay2.addLayout(self.gridLay2)

    self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
    self.horizontalLayout.addWidget(self.treeview)
    self.horizontalLayout.addLayout(self.verLay2)

    self.setCentralWidget(self.centralWidget)

    self.resize(1200, 600)
    self.setWindowTitle("FSEC plotter 2")

  def redraw(self):
    try:
      data = self.model.get_current_data()
    except NoSectionError as e:
      # if invalid section was selected, display the warning window.
      mes = e.args[0]
      QtWidgets.QMessageBox.warning(self, "FSEC plotter2", mes, 
        QtWidgets.QMessageBox.Ok)
      return
    self.plotarea.plot_fig(data)

  def save_figure(self):
    pass


if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)

  win = MainWindow()
  win.show()

  app.exec_()
