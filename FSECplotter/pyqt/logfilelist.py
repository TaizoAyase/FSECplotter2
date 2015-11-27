#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.core.logfile import *
import os

COLOR_LIST = [
  QtGui.QBrush(QtGui.QColor(255, 255, 255)),
  QtGui.QBrush(QtGui.QColor(240, 240, 240))
]

class LogfileModel(QtGui.QStandardItemModel):
  """ The class that has logfile-ary. 
      Also this is a model for ListView. """

  Default_Detector = "B"
  Default_Channel = 2

  def __init__(self, row, col, parent = None):
    super(LogfileModel, self).__init__(row, col, parent)
    self.logfiles = {}
    self.__id_count = 1

    # set header data
    self.headers = ('Id', 'Filename', 'Flow rate(ml/min)', 'Detector', 'Channel')
    for i, item in enumerate(self.headers):
      self.setHeaderData(i, QtCore.Qt.Horizontal, item)

  def add_item(self, filename):
    new_log = self.__append_logfile(filename)

    row = self.rowCount()
    order = row + 1 # set plot order
    order = self.__id_count
    self.__id_count += 1
    data_ary = [order, 
                new_log.file_name, 
                new_log.flowrate(), 
                self.Default_Detector, 
                self.Default_Channel]

    for i in range(len(data_ary)):
      # create new Item and set texts in data_ary
      item = QtGui.QStandardItem()
      if i == 0:
        item.setCheckable(True)
        item.setCheckState(2) # take value of 0, 1 or 2 
      item.setText(str(data_ary[i]))
      item.setBackground(COLOR_LIST[row%2])

      self.setItem(row, i, item)

  def move_item(self, current_index, shift):
    next_row_num = current_index + int(shift)

    # if the top or bottom item is selected, beep and ignore
    if next_row_num < 0 or next_row_num == self.rowCount():
      QtWidgets.QApplication.beep()
      return current_index

    # pop the row and insert to new position
    target_row = self.takeRow(current_index)
    self.insertRow(next_row_num, target_row)
    return next_row_num

  def delete_item(self, row_num):
    # We also remove the item from logfile array
    target_row = self.takeRow(row_num)
    del_id = target_row[0].text()
    del_logfile = self.logfiles.pop(int(del_id))
    del target_row
    del del_logfile

  def mimeData(self, indexes):
    mimedata = QtCore.QMimeData() # create Mime Data
    urllist  = []
    for index in indexes:
      # if the index of column is 0, do nothing 
      if index.column() != 0:
        continue
 
      item     = self.itemFromIndex(index)
      filepath = item.text()

      # windows requires "/" in top
      # this not affect unix env.
      # and the urllist require the QUrl obj., 
      # cast the string to QUrl
      urllist.append(QtCore.QUrl('/' + filepath))
    mimedata.setUrls(urllist)
 
    return mimedata

  def get_current_data(self):
    data = {'filenames': [], 'flow_rates': [], 'data': []}
    for i in range(self.rowCount()):
      if self.item(i, 0).checkState() == 0:
        continue
      log_id = int(self.item(i, 0).text())
      detector = self.item(i, 3).text()
      channel_no = int(self.item(i, 4).text())
      sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)

      # set data ary
      filename = self.item(i, 1).text()
      try:
        data_table = self.logfiles[log_id].find_section(sec_name).data()
        data['data'].append(data_table)
        data['filenames'].append(filename)
        data['flow_rates'].append(self.item(i, 2).text())
      except NoSectionError:
        mes = "In the file '%s', section named '%s' is not exist." % (filename, sec_name)
        raise NoSectionError(mes)

    return data

  # private methods

  def __append_logfile(self, filename):
    abspath = os.path.abspath(filename)
    logfile = LogFile()
    logfile.parse(abspath)
    # Try to set flowrate of log
    try:
      logfile.flowrate()
    except NoMatchedFlowRateError:
      logfile.flow_rate = 0

    self.logfiles[self.__id_count] = logfile
    return logfile


class LogfileListView(QtWidgets.QTreeView):
  """List view for LogfileListView"""
  def __init__(self, parent = None):
    super(LogfileListView, self).__init__(parent)
    self.setAcceptDrops(True)
    self.setDragEnabled(True)
    #self.setSortingEnabled(True)
    self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

  def dragEnterEvent(self, event):
    mimedata = event.mimeData()
    if mimedata.hasUrls():
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    mimedata = event.mimeData()
    model = self.model()

    if mimedata.hasUrls():
      urllist = mimedata.urls()
      for url in urllist:
        model.add_item(url.path())
      event.accept()
    else:
      event.ignore()


class LogfileListWidget(QtWidgets.QWidget):
  """Widget for control the logfiles"""
  def __init__(self, parent = None):
    super(LogfileListWidget, self).__init__(parent)

    # Standard item model
    self.model = LogfileModel(0, 5, self)
    self.selection_model = QtCore.QItemSelectionModel(self.model)

    self.treeview = LogfileListView(self)

    # set ItemModel to treeview widget
    self.treeview.setModel(self.model)
    self.treeview.setSelectionModel(self.selection_model)

    # TreeView setting
    #self.treeview.setColumnWidth(1, 140)
    self.treeview.setSelectionMode(
      QtWidgets.QAbstractItemView.ExtendedSelection
    )
    self.selection_model.clear()

    # set buttons
    self.open_button = QtWidgets.QPushButton(self)
    self.open_button.setObjectName("Open button")
    self.open_button.setText("Open file")

    self.delete_button = QtWidgets.QPushButton(self)
    self.delete_button.setObjectName("Delete button")
    self.delete_button.setText("Remove file")

    self.move_up_button = QtWidgets.QPushButton(self)
    self.move_up_button.setObjectName("Move-up button")
    self.move_up_button.setText("Move up")
    self.move_down_button = QtWidgets.QPushButton(self)
    self.move_down_button.setObjectName("Move-down button")
    self.move_down_button.setText("Move down")

    self.gridLay1 = QtWidgets.QGridLayout()
    self.gridLay1.addWidget(self.open_button, 0, 0, 1, 1)
    self.gridLay1.addWidget(self.delete_button, 0, 1, 1, 1)
    self.gridLay1.addWidget(self.move_up_button, 1, 0, 1, 1)
    self.gridLay1.addWidget(self.move_down_button, 1, 1, 1, 1)

    self.verLay1 = QtWidgets.QVBoxLayout()
    self.verLay1.addWidget(self.treeview)

    self.verLay2 = QtWidgets.QVBoxLayout(self)
    self.verLay2.addLayout(self.verLay1)
    self.verLay2.addLayout(self.gridLay1)

    # signal slot definition
    self.open_button.clicked.connect(self.open_file)
    self.delete_button.clicked.connect(self.delete_file)
    self.move_up_button.clicked.connect(lambda: self.move_selected(-1))
    self.move_down_button.clicked.connect(lambda: self.move_selected(1))

  def open_file(self):
    # open the file selection dialog
    # enable multiple selection
    filename = QtWidgets.QFileDialog.getOpenFileNames(
      self, "Open file", os.path.expanduser('~'))
    for f in filename[0]:
      self.model.add_item(f)

  def delete_file(self):
    try:
      current_row = self.__get_current_index()
    except IndexOutOfRangeError:
      return
    self.model.delete_item(current_row)
    self.selection_model.clear()

  def move_selected(self, shift):
    try:
      current_row = self.__get_current_index()
    except IndexOutOfRangeError:
      return
    moved_to = self.model.move_item(current_row, int(shift))

    # set selection to moved row
    self.selection_model.clear()

    left_idx = self.model.index(moved_to, 0, QtCore.QModelIndex())
    right_idx = self.model.index(moved_to, self.model.columnCount() - 1)
    row_selection = QtCore.QItemSelection()
    row_selection.select(left_idx, right_idx)

    self.selection_model.setCurrentIndex(left_idx, QtCore.QItemSelectionModel.Rows)
    self.selection_model.select(row_selection, QtCore.QItemSelectionModel.Select)

  # private methods

  def __get_current_index(self):
    current_index = self.selection_model.currentIndex()
    current_row = current_index.row()
    if current_row == -1:
      QtWidgets.QApplication.beep()
      raise IndexOutOfRangeError
    return current_row


class IndexOutOfRangeError(Exception):
  pass
    

if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)
  
  win = LogfileListWidget()
  model = LogfileModel(0, 5, win)
  #win.setModel(model)

  win.show()

  app.exec_()