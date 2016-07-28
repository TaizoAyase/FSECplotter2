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
from scipy.optimize import curve_fit
import numpy as np

# force matplotlib to use PyQt5 backends
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

class TmFitDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.canvas = FigureCanvas(self.fig)
        self.axes.set_xlabel("Temperature [C]")
        self.axes.set_ylabel("Relative Intensity")
        self.axes.grid()

        self.hori_layout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.save_fig_button = QtWidgets.QPushButton()
        self.save_fig_button.setText("Save fitting curve")
        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText("OK")
        self.hori_layout.addItem(spacerItem)
        self.hori_layout.addWidget(self.save_fig_button)
        self.hori_layout.addWidget(self.ok_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addLayout(self.hori_layout)
        self.setLayout(layout)

        self.default_filename = "fsects_fitcurve.png"

        self.ok_button.clicked.connect(self.accept)
        self.save_fig_button.clicked.connect(self.save_fig)

    def fit(self, data_x, data_y):
        self.axes.plot(data_x, data_y, 'o')

        try:
            param, cov = curve_fit(self.__sigmoid, data_x, data_y, p0=(1.0, 55))
        except RuntimeError as e:
            mes = 'Curve fitting failed!\nPlease check the temperature.'
            QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes, QtWidgets.QMessageBox.Ok)
            return
        lin_x = np.arange(120, step=0.5)
        self.axes.plot(lin_x, self.__sigmoid(lin_x, *param))
        self.axes.set_title("Calculated Tm: %2.1f C" % param[1])
        self.axes.set_ylim(0, 1)
        self.canvas.draw()

    def save_fig(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", os.path.expanduser("~") + "/" + self.default_filename,
            filter="images (*.png *.jpg *.pdf)")
        file_save_to = filename[0]
        if not file_save_to:
            return
        self.fig.savefig(file_save_to, bbox_inches='tight')

    # private

    def __sigmoid(self, x, a, tm):
        return 1/(1 + np.exp(a * (x - tm)))
