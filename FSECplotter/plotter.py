#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from matplotlib.pyplot import figure
from .logfile import LogFile

class Plotter():
  def __init__(self, logfiles, sec_name):
    self.sec_to_plot = sec_name

    # setup plot env.
    self.__fig = figure()
    self.__axes = self.__fig.add_subplot(111)
    self.__axes.hold(True) # superimporse the all plots

    # get the information of logfiles
    self.__logfiles = [ LogFile().parse(f) for f in logfiles ]
    self.__data = [ log.find_section(sec_name).data() for log in self.__logfiles ]
    self.__filenames = [ log.file_name for log in self.__logfiles ]

  def make_plot(self):
    # at first, set flow rate for each logfile
    [log.flowrate() for log in self.__logfiles]

    for (log, df) in zip(self.__logfiles, self.__data):
      self.__axes.plot(df[:, 0] * log.flow_rate, df[:, 1])

    self.__axes.legend(self.__filenames)
    self.__axes.set_xlabel("Volume(ml)")
    self.__axes.set_ylabel("FL intensity")

  def show_plot(self):
    pass

  def save_plot(self, save_name):
    self.__fig.savefig(save_name)
    return None

  ### private methods


if __name__ == '__main__':
  from glob import glob

  files = glob("./test/fixture/test*.txt")

  detector = "B"
  channel_no = 2
  sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)
  plt = Plotter(files, sec_name)
  plt.make_plot()
  plt.save_plot("test.png")
