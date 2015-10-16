#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends import qt_compat

from FSECplotter.section import *
from FSECplotter.logfile import *
#from FSECplotter.plotter import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from numpy import pi
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from glob import glob
import sys

class PltCanvas(FigureCanvas):
  def __init__(self, parent = None):
    fig = Figure(figsize = (10, 8), dpi = 200)
    self.axes = fig.add_subplot(111)
    self.axes.hold(True)

    detector = "B"
    channel_no = 2
    logfiles = glob("./test/fixture/test*.txt")
    sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)

    self.logfiles = [ LogFile().parse(f) for f in logfiles ]
    self.data = [ log.find_section(sec_name).data() for log in self.logfiles ]
    self.filenames = [ log.file_name for log in self.logfiles ]

    # make plot
    [log.flowrate() for log in self.logfiles]

    for (log, df) in zip(self.logfiles, self.data):
      self.axes.plot(df[:, 0] * log.flow_rate, df[:, 1])

    self.axes.grid()
    self.axes.legend(self.filenames)
    self.axes.set_xlabel("Volume(ml)")
    self.axes.set_ylabel("FL intensity")

    # set canvas config
    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self, 
      QSizePolicy.Preferred, 
      QSizePolicy.Preferred)
    FigureCanvas.updateGeometry(self)

class MyButton(QWidget):
  def __init__(self, parent):
    super(MyButton, self).__init__(parent = None)

    nameLabel = QLabel("Name:")
    self.nameLine = QLineEdit()
    #self.submitButton = QPushButton("Submit")

    buttonLayout1 = QVBoxLayout()
    buttonLayout1.addWidget(nameLabel)
    buttonLayout1.addWidget(self.nameLine)
    #buttonLayout1.addWidget(self.submitButton)

    # omake no adress 
    nameLabel2 = QLabel("Adress:")
    self.nameLine2 = QLineEdit()
    self.submitButton2 = QPushButton("Submit")

    buttonLayout2 = QVBoxLayout()
    buttonLayout2.addWidget(nameLabel2)
    buttonLayout2.addWidget(self.nameLine2)
    buttonLayout2.addWidget(self.submitButton2)

    # connect
    self.submitButton2.clicked.connect(self.submitContact)

    # define layout
    mainLayout = QGridLayout()
    #mainLayout.addLayout(buttonLayout1, 0, 0)
    mainLayout.addLayout(buttonLayout1, 0, 0)
    mainLayout.addLayout(buttonLayout2, 1, 0)

    self.setLayout(mainLayout)
    self.setWindowTitle("Hello Qt")

  def submitContact(self):
    name = self.nameLine.text()
    adress = self.nameLine2.text()

    #if name == "":
    #  QMessageBox.information(self, "Empty field", "Please enter a name and adress.")
    #  return
    #else:
    #  QMessageBox.information(self, "Success!", "Hello %s!" % name)

    if name == "":
      QMessageBox.information(self, "Empty field", "Please enter your name.")
      return 
    elif adress == "":
      QMessageBox.information(self, "Empty field", "Please enter your adress.")
      return
    else:
      QMessageBox.information(self, "Succsess!", "Hello %s at %s" % (name, adress))


class App(QMainWindow):
  def __init__(self, files, sec_name):
    QMainWindow.__init__(self, parent = None)

    #self.plotter = Plotter(files, sec_name)
    self.file_menu = QMenu('&File', self)
    self.file_menu.addAction('&Quit', self.fileQuit,
                                 Qt.CTRL + Qt.Key_Q)
    self.menuBar().addMenu(self.file_menu)

    self.help_menu = QMenu('&Help', self)
    self.menuBar().addSeparator()
    self.menuBar().addMenu(self.help_menu)

    self.help_menu.addAction('&About', self.about)

    self.main_widget = QWidget(self)

    detector = "B"
    channel_no = 2
    files = glob("./test/fixture/test*.txt")
    sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)

    l = QHBoxLayout(self.main_widget)
    #sc = PltCanvas(self.main_widget)
    sc = PltCanvas(parent = self.main_widget)
    #dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
    bt = MyButton(self.main_widget)

    l.addWidget(bt)
    l.addWidget(sc)
    #l.addWidget(dc)

    self.main_widget.setFocus()
    self.setCentralWidget(self.main_widget)

    self.statusBar().showMessage("All hail matplotlib!", 2000)

  def fileQuit(self):
    self.close()

  def closeEvent(self, ce):
    self.fileQuit()

  def about(self):
    QMessageBox.about(self, "About",
"hogehoge help message"
)



### main ###
detector = "B"
channel_no = 2
files = glob("./test/fixture/test*.txt")
sec_name = "LC Chromatogram(Detector %s-Ch%d)" % (detector, channel_no)


qApp = QApplication(sys.argv)
aw = App(files, sec_name)
aw.show()
sys.exit(qApp.exec_())