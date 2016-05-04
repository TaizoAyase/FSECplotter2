#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.models.logfilelist_model import *
from FSECplotter.core.logfile import LogfileError
from FSECplotter.core.shimadzu import NoMatchedFlowRateError, NoSectionError
import platform
import os


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

        # set progress bar dialog
        dlg = QtWidgets.QProgressDialog("Loading files ...", "Cancel", 0, 0, self)
        dlg.setValue(0)
        dlg.setWindowTitle("FSEC plotter 2")
        dlg.setWindowModality(QtCore.Qt.WindowModal)
        dlg.setCancelButton(None)
        dlg.setRange(0, len(filelist))
        dlg.show()

        for i, filepath in enumerate(filelist):
            # remove first slash if runs on windows
            # or, do nothing
            try:
                # set progress dialog
                dlg.setValue(i+1)
                filename = os.path.basename(filepath)
                mes = "Loading %s ..." % filename
                dlg.setLabelText(mes)

                model.add_item(filepath)

                QtWidgets.QApplication.processEvents()
            except NoMatchedFlowRateError as e:
                mes = e.args[0]
                QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                    QtWidgets.QMessageBox.Ok)
            except LogfileError as e:
                mes = e.args[0]
                QtWidgets.QMessageBox.critical(self, "FSEC plotter 2", mes,
                    QtWidgets.QMessageBox.Ok)

        # finish progress dialog
        dlg.hide()
