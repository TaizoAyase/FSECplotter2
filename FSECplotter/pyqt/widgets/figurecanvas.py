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
import numpy as np

# force matplotlib to use PyQt5 backends
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# FigureCanvas inherits QWidget
class Figurecanvas(FigureCanvas):

    SEABORN_STYLE = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
    SEABORN_CONTEXT = [None, 'paper', 'notebook', 'talk', 'poster']

    def __init__(self, parent=None, 
                 width=4, height=3, dpi=100, 
                 use_seaborn=False,
                 style=0, context=0):
        self.seaborn = use_seaborn
        if use_seaborn:
            import seaborn as sns
            sns.set_style(self.SEABORN_STYLE[style])
            sns.set_context(self.SEABORN_CONTEXT[context])

        # set matplitlib figure object
        self.fig = Figure(figsize=(width, height), dpi=int(dpi))
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
        if not self.seaborn:
            # this is omitted when using seaborn
            self.axes.grid()

        # if current_data has no data, return
        if current_data['total_data'] == 0:
            return

        # iterate for the length of dataset( len(filename) )
        num_data = len(current_data['filenames'])
        num_color = current_data['total_data']
        self.axes.set_color_cycle([self.__cm(1.*i/num_color) for i in range(num_color)])
        for i in range(num_data):
            x = current_data['data'][i][:, 0]
            y = current_data['data'][i][:, 1]

            x *= current_data['flowrate'][i]

            # set color
            col = current_data['color'][i]
            # if default, use default rainbow
            if col is None:
                col = self.__conv_to_hex(self.__cm(1.*i/num_color))

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

    # private

    def __adjust_scale(self, num_data):
        # in this scheme, at 16 sample, top~0.25,
        # which is the smallest size of graph-area
        if num_data < 16:
            adj = 0.9 - 0.04 * num_data
        else:
            adj = 0.25

        self.fig.subplots_adjust(top=adj)

    def __conv_to_hex(self, rgba_col):
        red = int(rgba_col[0] * 255)
        green = int(rgba_col[1] * 255)
        blue = int(rgba_col[2] * 255)
        return '#{r:02x}{g:02x}{b:02x}'.format(r=red, g=green, b=blue)

