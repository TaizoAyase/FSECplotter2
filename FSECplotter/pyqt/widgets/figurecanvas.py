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
class Figurecanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        # set matplitlib figure object
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)

        # call constructor of FigureCanvas
        super(Figurecanvas, self).__init__(self.fig)
        self.setParent(parent)

        # expand plot area as large as possible
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.x_min = 0
        self.x_max = 30

        # set color map object
        self.__cm = matplotlib.cm.gist_rainbow

    def plot_fig(self, current_data, linewidth):
        self.axes.clear()
        self.axes.grid()

        # iterate for the length of dataset( len(filename) )
        num_data = len(current_data['filenames'])
        num_color = current_data['total_data']
        self.axes.set_color_cycle(
            [self.__cm(1.*i/num_color) for i in range(num_color)])
        for i in range(num_data):
            x = current_data['data'][i][:, 0]
            y = current_data['data'][i][:, 1]
            col = current_data['color'][i]

            self.axes.plot(x, y, label=current_data['filenames'][i],
                           visible=current_data['enable_flags'][i],
                           linewidth=linewidth, color=col)

        self.axes.set_xlim(self.x_min, self.x_max)

        if self.y_min and self.y_max:
            self.axes.set_ylim(self.y_min, self.y_max)

        self.axes.legend(loc=3, mode="expand",
                         borderaxespad=0.,
                         bbox_to_anchor=(0., 1.02, 1., .102),
                         prop={'size': 'small'})
        self.axes.set_xlabel("Volume(ml)")
        self.axes.set_ylabel("FL intensity(AU)")
        self.__adjust_scale(num_data)
        self.draw()

    def save_fig_to(self, filepath):
        self.fig.savefig(filepath, bbox_inches='tight')

    def set_xlim(self, x_min, x_max):
        if not x_min:
            self.x_min = 0.
        else:
            self.x_min = float(x_min)

        if not x_max:
            self.x_max = 30.
        else:
            self.x_max = float(x_max)

        # avoid the illegal range setting
        if self.x_min > self.x_max:
            self.x_max = self.x_min + 1.0

        return self.x_min, self.x_max

    def set_ylim(self, y_min, y_max):
        # add 0.1 to raw value to avoid the False judge in if statement
        if not y_min:
            self.y_min = None
        elif y_min == "-":
            self.y_min = None
        else:
            self.y_min = float(y_min) + 0.1

        if not y_max:
            self.y_max = None
        elif y_max == "-":
            self.y_max = None
        else:
            self.y_max = float(y_max) + 0.1

        if not (self.y_min and self.y_max):
            return

        # avoid the illegal range setting
        if self.y_min > self.y_max:
            self.y_max = self.y_min + 100.0

        return self.y_min, self.y_max

    def __adjust_scale(self, num_data):
        # in this scheme, at 16 sample, top~0.25,
        # which is the smallest size of graph-area
        if num_data < 16:
            adj = 0.9 - 0.04 * num_data
        else:
            adj = 0.25

        self.fig.subplots_adjust(top=adj)
