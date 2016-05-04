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

        if mimedata.hasUrls():
            urllist = mimedata.urls()
            # modify urls for windows file path
            filelist = [url.path()[1:] if self.__windows_flag else url.path() for url in urllist]
            self.add_items(filelist)
            event.accept()
        else:
            event.ignore()

    def add_items(self, filelist):
        model = self.model()
        for filepath in filelist:
            # remove first slash if runs on windows
            # or, do nothing
            try:
                model.add_item(filepath)
            except NoMatchedFlowRateError as e:
                mes = e.args[0]
                QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                    QtWidgets.QMessageBox.Ok)
            except LogfileError as e:
                mes = e.args[0]
                QtWidgets.QMessageBox.critical(self, "FSEC plotter 2", mes,
                    QtWidgets.QMessageBox.Ok)
