#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2016, TaizoAyase, tikuta, biochem-fan

This file is part of FSECplotter2.

FSECplotter2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter import calc_yscale_factor, get_enabled_filename
from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *
from FSECplotter.pyqt.dialogs.yscale_dialog import *
from FSECplotter.pyqt.dialogs.tmcalc_dialog import *
from FSECplotter.pyqt.dialogs.tmfit_dialog import *
from FSECplotter.pyqt.dialogs.integrator_dialog import *
from FSECplotter.pyqt.dialogs.integrate_plot_dialog import *
from FSECplotter.pyqt.dialogs.preference_dialog import *
from FSECplotter.pyqt.dialogs.peaktable_dialog import *
import numpy as np

ORG_NAME = "TaizoAyase" # temporary org. name
APP_NAME = "FSECplotter2"

DEFAULTS = {
    'detector': 1,
    'channel': 1,
    'flowrate': 10.0,
    'linewidth': 1.0,
    'ts_gain': 1.0,
    'ts_tm': 50,
    'figure_dpi': 100
}

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
        self.setWindowTitle(APP_NAME)

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.readSettings()

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

        # tools menu
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

        # peak integration
        self.integrateAction = QtWidgets.QAction("Peak integration", self)
        self.integrateAction.setShortcut("Ctrl+I")
        self.integrateAction.setStatusTip("Peak integration.")
        self.integrateAction.triggered.connect(self.integrate)

        # peak table
        self.peaktableAction = QtWidgets.QAction("Peak table", self)
        self.peaktableAction.setShortcut("Ctrl+P")
        self.peaktableAction.setStatusTip("Create max-peak table in selected range.")
        self.peaktableAction.triggered.connect(self.peaktable)

        # option menu
        self.preferenceAction = QtWidgets.QAction("Preference", self)
        self.preferenceAction.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.preferenceAction.triggered.connect(self.preference)


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

        self.editMenu.addSeparator()
        self.editMenu.addAction(self.preferenceAction)

        # tool menu
        self.toolMenu = self.menuBar().addMenu("Tools")
        self.toolMenu.addAction(self.tsAction)
        self.toolMenu.addAction(self.y_scalingAction)
        self.toolMenu.addAction(self.integrateAction)
        self.toolMenu.addAction(self.peaktableAction)

        # option menu
        #self.optionMenu = self.menuBar().addMenu("Options")

    def createStatusBar(self):
        self.statusbar_label = QtWidgets.QLabel()
        self.statusbar_label.setIndent(3)

        self.statusBar().addWidget(self.statusbar_label)

        self.updateStatusBar()

    def updateStatusBar(self):
        pass

    def closeEvent(self, event):
        if self.okToContinue():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def okToContinue(self):
        if self.plotarea.modified:
            ret = QtWidgets.QMessageBox.warning(self, APP_NAME, 
              "The figure has been modified.\nDo you want to save your changes?",
              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
              QtWidgets.QMessageBox.Cancel)

            if ret == QtWidgets.QMessageBox.Yes:
                self.plotarea.save_figure()
                return True
            elif ret == QtWidgets.QMessageBox.Cancel:
                return False

        return True

    def readSettings(self):
        settings = QtCore.QSettings(ORG_NAME, APP_NAME)
        self.defaults = {}
        for k in DEFAULTS.keys():
            self.defaults[k] = settings.value(k)

        if None in self.defaults.values():
            self.defaults = DEFAULTS

        # TODO: reflect the setting of figure dpi value
        self.plotarea.updateDefaultParameters(**self.defaults)
        self.treeview.model.updateDefaultParameters(**self.defaults)

        del settings

    def writeSettings(self):
        settings = QtCore.QSettings(ORG_NAME, APP_NAME)

        for k, v in self.defaults.items():
            settings.setValue(k, float(v))

    def fsec_ts(self):
        n = self.treeview.model.rowCount()
        filenames = get_enabled_filename(self.treeview.model)
        tm_dialog = TmCalcDialog(self.treeview.model, self)

        # show in modeless dialog
        tm_dialog.show()

    def y_scaling(self):
        n = self.treeview.model.rowCount()
        filenames = get_enabled_filename(self.treeview.model)
        y_scale_dialog = YaxisScaleDialog(filenames, self)

        # show in modal dialog
        if y_scale_dialog.exec_():
            min_volume = y_scale_dialog.ui.lineEdit.text()
            max_volume = y_scale_dialog.ui.lineEdit_2.text()
            #c_volume = y_scale_dialog.ui.lineEdit.text()
            #file_norm = y_scale_dialog.ui.filename_for_normal.currentIndex()

            scale_factor = calc_yscale_factor(self.treeview.model, float(min_volume), float(max_volume))
            self.plotarea.rescale(scale_factor)

    def integrate(self):
        filenames = get_enabled_filename(self.treeview.model)
        integrator_dialog = IntegratorDialog(self)

        # show in modal dialog
        if integrator_dialog.exec_():
            min_volume = integrator_dialog.ui.lineEdit.text()
            max_volume = integrator_dialog.ui.lineEdit_2.text()

            int_ary = self.__peak_integrate(float(min_volume), float(max_volume))
            plot_dialog = IntegratePlotDialog(self)
            plot_dialog.plot(filenames, int_ary)
            plot_dialog.exec_()

    def peaktable(self):
        peaktable_dialog = PeakTableDialog(self.treeview.model, self)
        peaktable_dialog.show()

    def preference(self):
        dialog = PreferenceDialog(self.defaults, self)
        if dialog.exec_():
            #dialog.rejected.connect(lambda x:return)
            self.defaults = dialog.get_params()
            self.plotarea.updateDefaultParameters(**self.defaults)
            self.treeview.model.updateDefaultParameters(**self.defaults)

    # private

    def __peak_integrate(self, min_vol, max_vol):
        # select enebled data
        data = self.treeview.model.get_current_data()
        data_ary = [d for d, f in zip(data['data'], data['enable_flags']) if f]

        # get nearest indices to the min/max value
        min_idx = [np.argmin(np.abs(d[:, 0] - min_vol)) for d in data_ary]
        max_idx = [np.argmin(np.abs(d[:, 0] - max_vol)) for d in data_ary]

        delx_val_ary = [
            d[min_x+1:max_x+1, 0] - d[min_x:max_x, 0] for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
        ]
        y_val_ary = [
            d[min_x:max_x, 1] for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
        ]

        # sum over the product of (delta * y) for each data
        prod_val = [
            sum(delta * val) for delta, val in zip(delx_val_ary, y_val_ary)
        ]

        return prod_val


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
