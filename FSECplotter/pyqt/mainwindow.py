#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *
from FSECplotter.pyqt.dialogs.yscale_dialog import *
from FSECplotter.pyqt.dialogs.tmcalc_dialog import *
from FSECplotter.pyqt.dialogs.tmfit_dialog import *
import numpy as np


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.splitter = QtWidgets.QSplitter(self)

        # set list view and plot widgets
        self.treeview = LogfileListWidget(self)
        self.plotarea = PlotArea(self.treeview.model, self)

        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.plotarea)

        self.setCentralWidget(self.splitter)

        self.resize(1200, 600)
        self.setWindowTitle("FSEC plotter 2")

        self.createActions()
        self.createMenus()
        self.createStatusBar()

    def createActions(self):
        # file-menu
        # open
        self.openAction = QtWidgets.QAction("Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open the new log file.")
        self.openAction.triggered.connect(self.treeview.open_file)

        # save figure
        self.saveAsAction = QtWidgets.QAction("Save fig as ...", self)
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.setStatusTip("Save current figure as new name.")
        self.saveAsAction.triggered.connect(self.plotarea.save_figure)

        # quick save fig
        self.quickSaveAction = QtWidgets.QAction("Quick save", self)
        self.quickSaveAction.setShortcut("Ctrl+S")
        self.quickSaveAction.setStatusTip("One click save.")
        self.quickSaveAction.triggered.connect(self.plotarea.quick_save_figure)

        # remove all list items
        self.removeAllItemsAction = QtWidgets.QAction("Remove all files", self)
        self.removeAllItemsAction.setStatusTip("Remove all files from list.")
        self.removeAllItemsAction.triggered.connect(
            self.treeview.delete_all_files)

        # app quit
        self.quitAction = QtWidgets.QAction("Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit app.")
        self.quitAction.triggered.connect(
            QtWidgets.QApplication.closeAllWindows)

        # edit menu
        # redraw
        self.redrawAction = QtWidgets.QAction("Rdraw", self)
        self.redrawAction.setShortcut("Ctrl+R")
        self.redrawAction.setStatusTip("Force redraw plot.")
        self.redrawAction.triggered.connect(self.plotarea.redraw)

        # x-axis
        self.selectVolume = QtWidgets.QAction("Volume [mL]", self, checkable=True)
        self.selectVolume.setChecked(True)
        self.selectTime = QtWidgets.QAction("Time [min]", self, checkable=True)

        # tools-menu
        # fsec-ts
        self.tsAction = QtWidgets.QAction("calc Tm", self)
        self.tsAction.setShortcut("Ctrl+T")
        self.tsAction.setStatusTip("Calc Tm from FSEC-TS data.")
        self.tsAction.triggered.connect(self.fsec_ts)

        # scale y-axis
        self.y_scalingAction = QtWidgets.QAction("Y-axis scaling", self)
        self.y_scalingAction.setShortcut("Ctrl+Y")
        self.y_scalingAction.setStatusTip("Y-axis scaling.")
        self.y_scalingAction.triggered.connect(self.y_scaling)

    def createMenus(self):
        # file menu
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.quickSaveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.removeAllItemsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        # edit menu
        self.editMenu = self.menuBar().addMenu("Edit")
        self.editMenu.addAction(self.redrawAction)
        self.editsubMenu = self.editMenu.addMenu("X-axis")
        ag = QtWidgets.QActionGroup(self, exclusive=True)
        ag.addAction(self.selectVolume)
        ag.addAction(self.selectTime)
        self.editsubMenu.addAction(self.selectVolume)
        self.editsubMenu.addAction(self.selectTime)

        self.editsubMenu.addAction(self.selectVolume)
        self.editsubMenu.addAction(self.selectTime)

        # tool menu
        self.toolMenu = self.menuBar().addMenu("Tools")
        self.toolMenu.addAction(self.tsAction)
        self.toolMenu.addAction(self.y_scalingAction)

    def createStatusBar(self):
        self.statusbar_label = QtWidgets.QLabel()
        self.statusbar_label.setIndent(3)

        self.statusBar().addWidget(self.statusbar_label)

        self.updateStatusBar()

    def updateStatusBar(self):
        pass

    def fsec_ts(self):
        n = self.treeview.model.rowCount()
        filenames = self.__get_enabled_filename()
        tm_dialog = TmCalcDialog(filenames, self)

        if tm_dialog.exec_():
            c_volume = tm_dialog.ui.lineEdit.text()
            file_norm = tm_dialog.ui.comboBox.currentIndex()
            temp_list = tm_dialog.get_temperature()
            scale_factor = self.__y_scale(float(c_volume), file_norm)

            plot_dialog = TmFitDialog(self)
            x = np.array(temp_list)
            plot_dialog.fit(x, scale_factor)
            plot_dialog.exec_()

    def y_scaling(self):
        n = self.treeview.model.rowCount()
        filenames = self.__get_enabled_filename()
        y_scale_dialog = YaxisScaleDialog(filenames, self)

        if y_scale_dialog.exec_():
            c_volume = y_scale_dialog.ui.lineEdit.text()
            file_norm = y_scale_dialog.ui.filename_for_normal.currentIndex()
            scale_factor = self.__y_scale(float(c_volume), file_norm)
            self.plotarea.rescale(scale_factor)

    # private

    def __get_enabled_filename(self):
        data = self.treeview.model.get_current_data()
        ary = []
        for f, flag in zip(data['filenames'], data['enable_flags']):
            if not flag:
                continue
            ary.append(f)

        del data
        return ary

    def __y_scale(self, center_v, f_idx):
        data = self.treeview.model.get_current_data()
        data_ary = [d for d, f in zip(data['data'], data['enable_flags']) if f]
        idx_ary = [np.argmin(np.abs(d[:, 0] - center_v)) for d in data_ary]
        intensity_ary = [d[i, 1] for i, d in zip(idx_ary, data_ary)]
        norm_val = intensity_ary[f_idx]
        scale_factor = intensity_ary / norm_val
        return scale_factor


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
