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
    pass

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
    self.setSortingEnabled(True)
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



if __name__ == '__main__':
  import sys
  app = QtWidgets.QApplication(sys.argv)
  
  win = LogfileListView()
  model = LogfileModel(0, 5, win)
  win.setModel(model)

  win.show()

  app.exec_()