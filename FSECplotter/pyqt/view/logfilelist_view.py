#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.core.logfile import *
from FSECplotter.pyqt.models.logfilelist_model import *
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

                model.add_item(filepath)
            event.accept()
        else:
            event.ignore()
