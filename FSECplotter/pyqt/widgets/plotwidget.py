#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/Users/takemotomizuki/Documents/Dropbox/python/FSECplotter_py")
from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.widgets.figurecanvas import *
from FSECplotter.core.logfile import NoSectionError


# FigureCanvas inherits QWidget
class PlotArea(QtWidgets.QWidget):

    def __init__(self, parent=None):
        # call constructor of FigureCanvas
        super(PlotArea, self).__init__(parent)

        self.figcanvas = Figurecanvas(self)

        # set buttons
        self.redraw_button = QtWidgets.QPushButton(self)
        self.redraw_button.setObjectName("Redraw button")
        self.redraw_button.setText("Redraw")

        self.savefig_button = QtWidgets.QPushButton(self)
        self.savefig_button.setObjectName("Save Fig. button")
        self.savefig_button.setText("Save Fig. As ...")

        self.quick_save_button = QtWidgets.QPushButton(self)
        self.quick_save_button.setObjectName("Quick Save button")
        self.quick_save_button.setText("Quick Save")

        # set textbox
        self.xlim_min_box_label = QtWidgets.QLabel("x min:")
        self.xlim_min_box = QtWidgets.QLineEdit(self)
        self.xlim_min_box_label.setBuddy(self.xlim_min_box)
        self.xlim_min_box.setText("0")

        self.xlim_max_box_label = QtWidgets.QLabel("x max:")
        self.xlim_max_box = QtWidgets.QLineEdit(self)
        self.xlim_max_box_label.setBuddy(self.xlim_max_box)
        self.xlim_max_box.setText("30")

        self.double_valid = QtGui.QDoubleValidator()
        self.xlim_min_box.setValidator(self.double_valid)
        self.xlim_max_box.setValidator(self.double_valid)

        # right-hand layout
        self.horiLay1 = QtWidgets.QHBoxLayout()
        self.horiLay1.addWidget(self.xlim_min_box_label)
        self.horiLay1.addWidget(self.xlim_min_box)
        self.horiLay1.addWidget(self.xlim_max_box_label)
        self.horiLay1.addWidget(self.xlim_max_box)

        self.horiLay2 = QtWidgets.QHBoxLayout()
        self.horiLay2.addWidget(self.redraw_button)
        self.horiLay2.addWidget(self.savefig_button)
        self.horiLay2.addWidget(self.quick_save_button)

        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.addLayout(self.horiLay1)
        self.buttons_layout.addLayout(self.horiLay2)

        self.verLay1 = QtWidgets.QVBoxLayout(self)
        self.verLay1.addWidget(self.figcanvas)
        self.verLay1.addLayout(self.buttons_layout)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = PlotArea()

    win.show()

    app.exec_()