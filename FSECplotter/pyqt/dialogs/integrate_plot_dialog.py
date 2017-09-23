#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2017, TaizoAyase, tikuta, biochem-fan

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

from PyQt5 import QtCore, QtGui, QtWidgets
from scipy.optimize import curve_fit
import numpy as np

# force matplotlib to use PyQt5 backends
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class IntegratePlotDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.canvas = FigureCanvas(self.fig)
        self.axes.set_ylabel("Integrated intensity")
        self.axes.set_title("Peak Integration")
        self.axes.grid()

        self.hori_layout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.save_fig_button = QtWidgets.QPushButton()
        self.save_fig_button.setText("Save barplot")

        self.save_csv_button = QtWidgets.QPushButton()
        self.save_csv_button.setText("Save CSV")

        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText("OK")

        self.hori_layout.addItem(spacerItem)
        self.hori_layout.addWidget(self.save_fig_button)
        self.hori_layout.addWidget(self.save_csv_button)
        self.hori_layout.addWidget(self.ok_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addLayout(self.hori_layout)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.save_csv_button.clicked.connect(self.save_csv)
        self.save_fig_button.clicked.connect(self.save_fig)

        # set variables
        self.filenames = None
        self.intensities= None

        self.default_table_filename = "integrate_table.csv"
        self.default_plot_filename = "integrate.png"

    def plot(self, filenames, values):
        x = np.arange(len(filenames))

        self.axes.bar(x, values, 
            align="center", 
            width=0.4)
        self.axes.set_xticklabels(filenames, rotation=45)

        self.axes.set_xlabel('file ID')
        self.axes.set_ylabel('integrated intensity')

        self.canvas.draw()

        # set values to write out csv file
        self.filenames = filenames
        self.intensities = [str(v) for v in values]

    def save_csv(self):
        if (self.filenames is None) or (self.intensities is None):
            raise ArgumentError("The length of filenames and intensities is not match.")

        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save CSV",
            os.path.expanduser("~") + "/" + self.default_table_filename,
            filter="Text files (*.csv)")
        file_save_to = filename[0]

        if not file_save_to:
            return

        text = ", ".join(self.filenames) + "\n" + ", ".join(self.intensities)
        with open(file_save_to, "w+") as f:
            f.write(text)

    def save_fig(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", 
            os.path.expanduser("~") + "/" + self.default_plot_filename,
            filter="images (*.png *.jpg *.pdf)")

        file_save_to = filename[0]
        if not file_save_to:
            return

        self.fig.savefig(file_save_to, bbox_inches='tight') 

