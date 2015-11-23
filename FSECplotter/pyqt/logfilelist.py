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
    self.logfiles = []

  def add_item(self, filename):
    new_log = self.__append_logfile(filename)

    row = self.rowCount()
    order = row + 1 # set plot order
    data_ary = [order, 
                new_log.file_name, 
                new_log.flow_rate, 
                self.Default_Detector, 
                self.Default_Channel]

    for i in range(len(data_ary)):
      # create new Item and set texts in data_ary
      item = QtGui.QStandardItem()
      item.setText(str(data_ary[i]))
      item.setBackground(COLOR_LIST[row%2])

      self.setItem(row, i, item)

  def delete_item(self, row_num):
    # We also remove the item from logfile array
    target_row = self.takeRow(row_num)
    #self.removeRow(row_num)

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
      detector = self.item(i, 3).text()
      channel_no = int(self.item(i, 4).text())
      sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)

      # set data ary
      data['filenames'].append(self.item(i, 1).text())
      data['flow_rates'].append(self.item(i, 2).text())
      # TODO: change this finding logic
      data['data'].append(self.logfiles[i].find_section(sec_name).data())

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
    self.logfiles.append(logfile)
    return logfile


class LogfileListView(QtWidgets.QTreeView):
  """docstring for LogfileListView"""
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

