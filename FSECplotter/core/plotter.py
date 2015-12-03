#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from matplotlib.pyplot import figure
from .logfile import LogFile


class Plotter():

    def __init__(self, logfiles, sec_name):
        self.sec_to_plot = sec_name

        # setup plot env.
        self.fig = figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)  # superimporse the all plots

        # get the information of logfiles
        self.logfiles = [LogFile().parse(f) for f in logfiles]
        self.data = [log.find_section(sec_name).data()
                     for log in self.logfiles]
        self.filenames = [log.file_name for log in self.logfiles]

    def make_plot(self):
        # at first, set flow rate for each logfile
        [log.flowrate() for log in self.logfiles]

        for (log, df) in zip(self.logfiles, self.data):
            self.axes.plot(df[:, 0] * log.flow_rate, df[:, 1])

        self.axes.grid()
        self.axes.legend(self.filenames)
        self.axes.set_xlabel("Volume(ml)")
        self.axes.set_ylabel("FL intensity")

    def show_plot(self):
        self.fig.show()

    def save_plot(self, save_name):
        self.fig.savefig(save_name)
        return None

    def xlim(xmin, xmax):
        self.axes.xlim(xmin, xmax)

    def ylim(ymin, ymax):
        self.axes.ylim(ymin, ymax)

    # private methods
