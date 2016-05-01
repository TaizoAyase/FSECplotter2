#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.models.logfilelist_model import *
from FSECplotter.core.logfile import LogfileError
from FSECplotter.core.shimadzu import NoMatchedFlowRateError, NoSectionError
import platform


class LogfileListView(QtWidgets.QTreeView):
    """List view for LogfileListView"""

    def __init__(self, parent=None):
        super(LogfileListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # self.setSortingEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.__windows_flag = platform.system() == "Windows"

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
                # remove first slash if runs on windows
                # or, do nothing
                path = url.path()
                filepath = path[1:] if self.__windows_flag else path

                try:
                    self.add_item(filepath)
                except NoMatchedFlowRateError as e:
                    mes = e.args[0]
                    QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                        QtWidgets.QMessageBox.Ok)
                except LogfileError as e:
                    mes = e.args[0]
                    QtWidgets.QMessageBox.critical(self, "FSEC plotter 2", mes,
                        QtWidgets.QMessageBox.Ok)
            event.accept()
        else:
            event.ignore()

    def add_item(self, filename):
        self.model().add_item(filename)

        col_button = QtWidgets.QPushButton('Default')
        row = self.model().rowCount() - 1
        idx = self.model().index(row, 5, QtCore.QModelIndex())
        self.setIndexWidget(idx, col_button)
