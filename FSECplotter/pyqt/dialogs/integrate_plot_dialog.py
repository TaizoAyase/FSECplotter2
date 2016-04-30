#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from scipy.optimize import curve_fit
import numpy as np

# force matplotlib to use PyQt5 backends
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

class IntegratePlotDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.canvas = FigureCanvas(self.fig)
        self.axes.set_ylabel("Integrated intensity")
        self.axes.grid()

        self.hori_layout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.save_fig_button = QtWidgets.QPushButton()
        self.save_fig_button.setText("Save barplot")

        self.save_csv_button = QtWidgets.QPushButton()
        sef.save_csv_button.setText("Save CSV")

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
        self.values = None

    def plot(self, filenames, values):
        x = np.arange(len(filenames))
        self.axes.bar(x, values, 
            align="center", 
            width=0.4, 
            tick_label=filenames)
        self.canvas.draw()

        # set values to write out csv file
        self.filenames = filenames
        self.intensities = values

    def save_csv(self):
        if (self.filenames is None) or (self.values is None):
            raise
        # TODO: implement me!
        pass

    def save_fig(self):
        default_filename = "integrate.png"
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", 
            os.path.expanduser("~") + "/" + default_filename,
            filter="images (*.png *.jpg *.pdf)")
        file_save_to = filename[0]
        if not file_save_to:
            return
        self.fig.savefig(file_save_to, bbox_inches='tight') 

