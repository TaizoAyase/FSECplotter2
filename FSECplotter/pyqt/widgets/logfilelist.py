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
from FSECplotter.pyqt.models.logfilelist_model import *
from FSECplotter.pyqt.view.logfilelist_view import *
import os
import platform


class LogfileListWidget(QtWidgets.QWidget):
    """Widget for control the logfiles"""

    def __init__(self, parent=None):
        super(LogfileListWidget, self).__init__(parent)

        # Standard item model
        self.model = LogfileModel(0, 6, self)
        self.selection_model = QtCore.QItemSelectionModel(self.model)

        self.treeview = LogfileListView(self)

        # set ItemModel to treeview widget
        self.treeview.setModel(self.model)
        self.treeview.setSelectionModel(self.selection_model)

        # TreeView setting
        self.treeview.setSelectionMode(
            QtWidgets.QAbstractItemView.ContiguousSelection
        )
        self.selection_model.clear()

        # set buttons
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Change all detector to:")
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Change all channel to:")
        self.setall_detector_comboBox = QtWidgets.QComboBox(self)
        self.setall_detector_comboBox.addItem("")
        self.setall_detector_comboBox.setItemText(0, "A")
        self.setall_detector_comboBox.addItem("")
        self.setall_detector_comboBox.setItemText(1, "B")
        self.setall_channel_comboBox = QtWidgets.QComboBox(self)
        self.setall_channel_comboBox.addItem("")
        self.setall_channel_comboBox.setItemText(0, "1")
        self.setall_channel_comboBox.addItem("")
        self.setall_channel_comboBox.setItemText(1, "2")

        self.combobox_layout = QtWidgets.QHBoxLayout()
        self.combobox_layout.addWidget(self.label1)
        self.combobox_layout.addWidget(self.setall_detector_comboBox)
        self.combobox_layout.addWidget(self.label2)
        self.combobox_layout.addWidget(self.setall_channel_comboBox)

        self.open_button = QtWidgets.QPushButton(self)
        self.open_button.setObjectName("Open button")
        self.open_button.setText("Open file")

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setObjectName("Remove file button")
        self.delete_button.setText("Remove file")

        self.color_button = QtWidgets.QPushButton(self)
        self.color_button.setObjectName("Change plot color")
        self.color_button.setText("Change color")

        self.reset_color_button = QtWidgets.QPushButton(self)
        self.reset_color_button.setObjectName("Reset color to default")
        self.reset_color_button.setText("Reset color")

        self.check_all_button = QtWidgets.QPushButton(self)
        self.check_all_button.setObjectName("Check all button")
        self.check_all_button.setText("Check All")
        self.uncheck_all_button = QtWidgets.QPushButton(self)
        self.uncheck_all_button.setObjectName("Uncheck all button")
        self.uncheck_all_button.setText("Uncheck All")

        self.move_up_button = QtWidgets.QPushButton(self)
        self.move_up_button.setObjectName("Move-up button")
        self.move_up_button.setText("Move up")
        self.move_down_button = QtWidgets.QPushButton(self)
        self.move_down_button.setObjectName("Move-down button")
        self.move_down_button.setText("Move down")

        self.gridLay1 = QtWidgets.QGridLayout()
        self.gridLay1.addWidget(self.open_button, 0, 0, 1, 1)
        self.gridLay1.addWidget(self.delete_button, 0, 1, 1, 1)
        self.gridLay1.addWidget(self.color_button, 0, 2, 1, 1)
        self.gridLay1.addWidget(self.reset_color_button, 0, 3, 1, 1)
        self.gridLay1.addWidget(self.check_all_button, 1, 0, 1, 1)
        self.gridLay1.addWidget(self.uncheck_all_button, 1, 1, 1, 1)
        self.gridLay1.addWidget(self.move_up_button, 1, 2, 1, 1)
        self.gridLay1.addWidget(self.move_down_button, 1, 3, 1, 1)

        self.verLay1 = QtWidgets.QVBoxLayout()
        self.verLay1.addWidget(self.treeview)

        self.verLay2 = QtWidgets.QVBoxLayout(self)
        self.verLay2.addLayout(self.combobox_layout)
        self.verLay2.addLayout(self.verLay1)
        self.verLay2.addLayout(self.gridLay1)

        # signal slot definition
        self.setall_detector_comboBox.activated.connect(
            self.change_all_detector)
        self.setall_channel_comboBox.activated.connect(
            self.change_all_channel)

        # buttons
        self.open_button.clicked.connect(self.open_file)
        self.delete_button.clicked.connect(self.delete_file)
        self.color_button.clicked.connect(self.change_plot_color)
        self.reset_color_button.clicked.connect(self.reset_color)

        self.check_all_button.clicked.connect(
            lambda: self.model.change_all_check_state(2))
        self.uncheck_all_button.clicked.connect(
            lambda: self.model.change_all_check_state(0))
        self.move_up_button.clicked.connect(lambda: self.move_selected(-1))
        self.move_down_button.clicked.connect(lambda: self.move_selected(1))

    def change_all_detector(self):
        det = self.setall_detector_comboBox.currentText()
        self.model.select_params_to(col=3, param=det)

    def change_all_channel(self):
        ch = self.setall_channel_comboBox.currentText()
        self.model.select_params_to(col=4, param=ch)

    def open_file(self):
        # open the file selection dialog
        # enable multiple selection
        filename = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open file", os.path.expanduser('~'))
        self.treeview.add_items(filename[0])

    def delete_file(self):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        self.model.delete_item(current_row)
        self.selection_model.clear()
        self.__select_row(current_row)

    def delete_all_files(self):
        while self.model.rowCount() > 0:
            self.model.delete_item(0)

    def change_plot_color(self):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        # get current color of selected row
        current_col = self.model.get_color(current_row)
        col_dlg = QtWidgets.QColorDialog(self)
        # if color is already set, set initial color to the current one
        if current_col:
            col_dlg.setCurrentColor(QtGui.QColor(current_col))

        # select the color
        if col_dlg.exec_():
            col_name = col_dlg.currentColor().name()
            self.model.set_color(current_row, col_name)

    def reset_color(self):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        self.model.reset_color(current_row)

    def move_selected(self, shift):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        moved_to = self.model.move_item(current_row, int(shift))
        self.selection_model.clear()
        self.__select_row(moved_to)

    def write_csv(self):
        pass

    # private methods

    def __get_current_index(self):
        current_index = self.selection_model.currentIndex()
        current_row = current_index.row()
        if current_row == -1:
            QtWidgets.QApplication.beep()
            raise IndexOutOfRangeError
        return current_row

    def __select_row(self, row_idx):
        left_idx = self.model.index(row_idx, 0, QtCore.QModelIndex())
        right_idx = self.model.index(row_idx, self.model.columnCount() - 1)
        row_selection = QtCore.QItemSelection()
        row_selection.select(left_idx, right_idx)

        self.selection_model.setCurrentIndex(
            left_idx, QtCore.QItemSelectionModel.Rows)
        self.selection_model.select(
            row_selection, QtCore.QItemSelectionModel.Select)


class IndexOutOfRangeError(Exception):
    pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = LogfileListWidget()
    model = LogfileModel(0, 5, win)
    # win.setModel(model)

    win.show()

    app.exec_()
