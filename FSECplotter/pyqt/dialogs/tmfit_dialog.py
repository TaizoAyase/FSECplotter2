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

class TmFitDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.canvas = FigureCanvas(self.fig)
        self.axes.set_xlabel("Temperature [C]")
        self.axes.set_ylabel("Relative Intensity")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def fit(self, data_x, data_y):
        self.axes.plot(data_x, data_y, 'o')

        param, cov = curve_fit(self.__sigmoid, data_x, data_y, p0=(1.0, 55))
        lin_x = np.arange(100, step=0.5)
        self.axes.plot(lin_x, self.__sigmoid(lin_x, *param))
        self.axes.set_title("Calculated Tm is %2.1f C" % param[1])
        self.axes.set_ylim(0, 1)
        self.canvas.draw()

    # private

    def __sigmoid(self, x, a, tm):
        return 1/(1 + np.exp(a * (x - tm)))
