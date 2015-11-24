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

    # Standard item model
    self.model = LogfileModel(0, 5, self)
    self.selection_model = QtCore.QItemSelectionModel(self.model)

    # set list view and plot widgets
    self.treeview = LogfileListView(self.centralWidget)
    self.plotarea = PlotArea(self.centralWidget)   

    # set ItemModel to treeview widget
    self.treeview.setModel(self.model)
    self.treeview.setSelectionModel(self.selection_model)
    headers = ('Order', 'Filename', 'Flow rate(ml/min)', 'Detector', 'Channel')
    for i, item in enumerate(headers):
      self.model.setHeaderData(i, QtCore.Qt.Horizontal, item)

    # make first plot
    data = self.model.get_current_data()
    self.plotarea.plot_fig(data)

    # TreeView setting
    #self.treeview.setColumnWidth(1, 140)
    self.treeview.setSelectionMode(
      QtWidgets.QAbstractItemView.ExtendedSelection
    )

    # set buttons
    self.redraw_button = QtWidgets.QPushButton(self.centralWidget)
    self.redraw_button.setObjectName("Redraw button")
    self.redraw_button.setText("Redraw")

    self.open_button = QtWidgets.QPushButton(self.centralWidget)
    self.open_button.setObjectName("Open button")
    self.open_button.setText("Open file")

    self.delete_button = QtWidgets.QPushButton(self.centralWidget)
    self.delete_button.setObjectName("Delete button")
    self.delete_button.setText("Remove file")

    self.move_up_button = QtWidgets.QPushButton(self.centralWidget)
    self.move_up_button.setObjectName("Move-up button")
    self.move_up_button.setText("Move up")
    self.move_down_button = QtWidgets.QPushButton(self.centralWidget)
    self.move_down_button.setObjectName("Move-down button")
    self.move_down_button.setText("Move down")

    # signale slot definition
    self.redraw_button.clicked.connect(self.redraw)
    self.open_button.clicked.connect(self.open_file)
    self.delete_button.clicked.connect(self.delete_file)
    self.move_up_button.clicked.connect(self.move_up_selected)
    self.move_down_button.clicked.connect(self.move_down_selected)

    self.model.itemChanged.connect(self.model.on_displayname_changed)

    # layout
    self.gridLay1 = QtWidgets.QGridLayout()
    self.gridLay1.addWidget(self.open_button, 0, 0, 1, 1)
    self.gridLay1.addWidget(self.delete_button, 0, 1, 1, 1)
    self.gridLay1.addWidget(self.move_up_button, 1, 0, 1, 1)
    self.gridLay1.addWidget(self.move_down_button, 1, 1, 1, 1)

    self.verLay1 = QtWidgets.QVBoxLayout()
    self.verLay1.addWidget(self.treeview)
    self.verLay1.addLayout(self.gridLay1)

    self.verLay2 = QtWidgets.QVBoxLayout()
    self.verLay2.addWidget(self.plotarea)
    self.verLay2.addWidget(self.redraw_button)

    self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
    self.horizontalLayout.addLayout(self.verLay1)
    self.horizontalLayout.addLayout(self.verLay2)

    self.setCentralWidget(self.centralWidget)

    self.resize(1200, 600)
    self.setWindowTitle("FSEC file viewer Demo")

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

  def open_file(self):
    # open the file selection dialog
    # enable multiple selection
    filename = QtWidgets.QFileDialog.getOpenFileNames(
      self, "Open file", os.path.expanduser('~'))
    for f in filename[0]:
      self.model.add_item(f)

  def delete_file(self):
    # TODO implement
    current_index = self.selection_model.currentIndex()
    current_row = current_index.row()
    self.model.delete_item(current_row)

  def move_up_selected(self):
    pass

  def move_down_selected(self):
    pass


if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)

  win = MainWindow()
  win.show()

  app.exec_()
