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
    self.redraw()

    # set buttons
    self.redraw_button = QtWidgets.QPushButton(self.centralWidget)
    self.redraw_button.setObjectName("Redraw button")
    self.redraw_button.setText("Redraw")

    self.savefig_button = QtWidgets.QPushButton(self.centralWidget)
    self.savefig_button.setObjectName("Save Fig. button")
    self.savefig_button.setText("Save Fig. As ...")

    self.quick_save_button = QtWidgets.QPushButton(self.centralWidget)
    self.quick_save_button.setObjectName("Quick Save button")
    self.quick_save_button.setText("Quick Save")

    # signal slot definition
    self.redraw_button.clicked.connect(self.redraw)
    self.savefig_button.clicked.connect(self.save_figure)
    self.quick_save_button.clicked.connect(self.quick_save_figure)

    # right-hand layout
    self.gridLay1 = QtWidgets.QGridLayout()
    self.gridLay1.addWidget(self.redraw_button, 0, 0, 1, 1)
    self.gridLay1.addWidget(self.savefig_button, 0, 1, 1, 1)
    self.gridLay1.addWidget(self.quick_save_button, 0, 2, 1, 1)

    self.verLay1 = QtWidgets.QVBoxLayout()
    self.verLay1.addWidget(self.plotarea)
    self.verLay1.addLayout(self.gridLay1)

    self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
    self.horizontalLayout.addWidget(self.treeview)
    self.horizontalLayout.addLayout(self.verLay1)

    self.setCentralWidget(self.centralWidget)

    self.resize(1200, 600)
    self.setWindowTitle("FSEC plotter 2")

  def redraw(self):
    try:
      data = self.treeview.model.get_current_data()
    except NoSectionError as e:
      # if invalid section was selected, display the warning window.
      mes = e.args[0]
      QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes, 
        QtWidgets.QMessageBox.Ok)
      return
    self.plotarea.plot_fig(data)

  def save_figure(self):
    filename = QtWidgets.QFileDialog.getSaveFileName(
      self, "Save file", os.path.expanduser('~') + "/plot.png", 
      filter = "images (*.png *.jpg *.pdf)")
    print(filename)
    file_save_to = filename[0]
    self.plotarea.save_fig_to(file_save_to)

  def quick_save_figure(self):
    file_save_to = os.path.expanduser('~') + "/plot.png"
    self.plotarea.save_fig_to(file_save_to)


if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)

  win = MainWindow()
  win.show()

  app.exec_()
