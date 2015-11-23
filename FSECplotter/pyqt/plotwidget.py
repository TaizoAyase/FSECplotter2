#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

# force matplotlib to use PyQt5 backends
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# FigureCanvas inherits QWidget
class PlotArea(FigureCanvas):
  def __init__(self, parent = None, width = 4, height = 3, dpi = 100):
    # set matplitlib figure object
    self.fig = Figure(figsize = (width, height), dpi = dpi)
    self.axes = self.fig.add_subplot(111)
    self.axes.hold(True)

    # call constructor of FigureCanvas
    super(PlotArea, self).__init__(self.fig)
    self.setParent(parent)

    # expand plot area as large as possible
    FigureCanvas.setSizePolicy(self,
      QtWidgets.QSizePolicy.Expanding,
      QtWidgets.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def plot_fig(self, data_ary):
    self.axes.clear()
    self.axes.grid()

    # iterate for the length of dataset( len(filename) )
    num_data = len(data_ary['filenames'])
    for i in range(num_data):
      x = data_ary['data'][i][:, 0] * float(data_ary['flow_rates'][i])
      y = data_ary['data'][i][:, 1]
      self.axes.plot(x, y)

    self.axes.legend(data_ary['filenames'])
    self.axes.set_xlabel("Volume(ml)")
    self.axes.set_ylabel("FL intensity(AU)")
    self.draw()
