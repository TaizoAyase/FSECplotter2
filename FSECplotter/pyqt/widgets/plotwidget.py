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

import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.widgets.figurecanvas import *
from FSECplotter.core.shimadzu import NoSectionError


# FigureCanvas inherits QWidget
class PlotArea(QtWidgets.QWidget):

    updateParameters = QtCore.pyqtSlot()

    def __init__(self, listmodel, parent=None, dpi=100,
                 seaborn=False, style=0, context=0):
        # call constructor of FigureCanvas
        super(PlotArea, self).__init__(parent)

        self.figcanvas = Figurecanvas(self, dpi=dpi, 
                                      use_seaborn=seaborn,
                                      style=style, context=context)
        self.model = listmodel

        # default params
        self.linewidth = 1.0

        # set buttons
        self.redraw_button = QtWidgets.QPushButton(self)
        self.redraw_button.setObjectName("Redraw button")
        self.redraw_button.setText("Redraw")

        self.savefig_button = QtWidgets.QPushButton(self)
        self.savefig_button.setObjectName("Save Fig. button")
        self.savefig_button.setText("Save Fig As ...")

        self.quick_save_button = QtWidgets.QPushButton(self)
        self.quick_save_button.setObjectName("Quick Save button")
        self.quick_save_button.setText("Quick Save")

        self.save_csv_table_button = QtWidgets.QPushButton(self)
        self.save_csv_table_button.setObjectName("Save CSV table button")
        self.save_csv_table_button.setText("Save CSV table")

        # set textbox
        # xlim
        self.xlim_min_box_label = QtWidgets.QLabel("x min:")
        self.xlim_min_box = QtWidgets.QLineEdit(self)
        self.xlim_min_box_label.setBuddy(self.xlim_min_box)
        self.xlim_min_box.setText("0")

        self.xlim_max_box_label = QtWidgets.QLabel("x max:")
        self.xlim_max_box = QtWidgets.QLineEdit(self)
        self.xlim_max_box_label.setBuddy(self.xlim_max_box)
        self.xlim_max_box.setText("30")

        # ylim
        self.ylim_min_box_label = QtWidgets.QLabel("y min:")
        self.ylim_min_box = QtWidgets.QLineEdit(self)
        self.ylim_min_box_label.setBuddy(self.ylim_min_box)

        self.ylim_max_box_label = QtWidgets.QLabel("y max:")
        self.ylim_max_box = QtWidgets.QLineEdit(self)
        self.ylim_max_box_label.setBuddy(self.ylim_max_box)

        regexp1 = QtCore.QRegExp('^\d+\.?\d*')
        self.double_valid1 = QtGui.QRegExpValidator(regexp1)
        self.xlim_min_box.setValidator(self.double_valid1)
        self.xlim_max_box.setValidator(self.double_valid1)

        regexp2 = QtCore.QRegExp('^-?\d+\.?\d*')
        self.double_valid2 = QtGui.QRegExpValidator(regexp2)
        self.ylim_min_box.setValidator(self.double_valid2)
        self.ylim_max_box.setValidator(self.double_valid2)

        # set spinbox
        # linewith
        self.linewidth_spinbox_label = QtWidgets.QLabel("Line width:")
        self.linewidth_spinbox = QtWidgets.QDoubleSpinBox(self)
        self.linewidth_spinbox.setSingleStep(0.5)
        self.linewidth_spinbox.setDecimals(1)
        self.linewidth_spinbox.setSuffix(" pt")
        self.linewidth_spinbox.setValue(self.linewidth)
        self.linewidth_spinbox_label.setBuddy(self.linewidth_spinbox)

        # right-hand layout
        self.horiLay1 = QtWidgets.QHBoxLayout()
        self.horiLay1.addWidget(self.xlim_min_box_label)
        self.horiLay1.addWidget(self.xlim_min_box)
        self.horiLay1.addWidget(self.xlim_max_box_label)
        self.horiLay1.addWidget(self.xlim_max_box)

        self.horiLay2 = QtWidgets.QHBoxLayout()
        self.horiLay2.addWidget(self.ylim_min_box_label)
        self.horiLay2.addWidget(self.ylim_min_box)
        self.horiLay2.addWidget(self.ylim_max_box_label)
        self.horiLay2.addWidget(self.ylim_max_box)

        self.horiLay3 = QtWidgets.QHBoxLayout()
        self.horiLay3.addWidget(self.redraw_button)
        self.horiLay3.addWidget(self.savefig_button)
        self.horiLay3.addWidget(self.quick_save_button)
        self.horiLay3.addWidget(self.save_csv_table_button)

        self.horiLay4 = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20, 
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horiLay4.addWidget(self.linewidth_spinbox_label)
        self.horiLay4.addWidget(self.linewidth_spinbox)
        self.horiLay4.addItem(spacerItem)

        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.addLayout(self.horiLay1)
        self.buttons_layout.addLayout(self.horiLay2)
        self.buttons_layout.addLayout(self.horiLay4)
        self.buttons_layout.addLayout(self.horiLay3)

        self.verLay1 = QtWidgets.QVBoxLayout(self)
        self.verLay1.addWidget(self.figcanvas)
        self.verLay1.addLayout(self.buttons_layout)

        # signal slot connection
        self.redraw_button.clicked.connect(self.redraw)
        self.savefig_button.clicked.connect(self.save_figure)
        self.quick_save_button.clicked.connect(self.quick_save_figure)
        self.xlim_min_box.textChanged.connect(self.redraw)
        self.xlim_max_box.textChanged.connect(self.redraw)
        self.ylim_min_box.textChanged.connect(self.redraw)
        self.ylim_max_box.textChanged.connect(self.redraw)
        self.linewidth_spinbox.valueChanged.connect(self.redraw)
        self.model.itemChanged.connect(self.redraw)

        # modified flag
        self.modified = False

    def updateDefaultParameters(self, **kwargs):
        self.linewidth = float(kwargs['linewidth'])
        self.linewidth_spinbox.setValue(self.linewidth)

    def redraw(self):
        try:
            data = self.model.get_current_data()
        except NoSectionError as e:
            # if invalid section was selected, display the warning window.
            mes = e.args[0]
            QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                                          QtWidgets.QMessageBox.Ok)
            return

        self.figcanvas.set_xlim(self.xlim_min_box.text(),
                                self.xlim_max_box.text())
        self.figcanvas.set_ylim(self.ylim_min_box.text(),
                                self.ylim_max_box.text())
        self.linewidth = self.linewidth_spinbox.value()
        self.figcanvas.plot_fig(data, self.linewidth)
        self.modified = True

    def save_figure(self):
        defalt_plot_name = time.strftime("%y%m%d_%H%M%S") + "_plot.png"
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", self.model.current_dir + "/" + defalt_plot_name,
            filter="images (*.png *.jpg *.pdf)")
        file_save_to = filename[0]
        # if filename is empty string, do nothing
        if not file_save_to:
            return
        self.figcanvas.save_fig_to(file_save_to)
        self.modified = False

    def quick_save_figure(self):
        defalt_plot_name = time.strftime("%y%m%d_%H%M%S") + "_plot.png"
        file_save_to = self.model.current_dir + "/" + defalt_plot_name
        self.figcanvas.save_fig_to(file_save_to)
        self.modified = False

    def rescale(self, scale_factor):
        try:
            data = self.model.get_current_data()
        except NoSectionError as e:
            # if invalid section was selected, display the warning window.
            mes = e.args[0]
            QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                                          QtWidgets.QMessageBox.Ok)
            return

        j = 0 # index for scale factor array
        for i, flag in enumerate(data['enable_flags']):
            # skip the non-enabled data
            if not flag:
                continue
            data['data'][i][:, 1] = data['data'][i][:, 1] / scale_factor[j]
            j += 1

        self.figcanvas.set_xlim(self.xlim_min_box.text(),
                                self.xlim_max_box.text())
        self.figcanvas.plot_fig(data, self.linewidth)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = PlotArea()
    win.show()

    app.exec_()
