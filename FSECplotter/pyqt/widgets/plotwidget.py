#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.pyqt.widgets.figurecanvas import *
from FSECplotter.core.logfile import NoSectionError


# FigureCanvas inherits QWidget
class PlotArea(QtWidgets.QWidget):

    def __init__(self, listmodel, parent=None):
        # call constructor of FigureCanvas
        super(PlotArea, self).__init__(parent)

        self.figcanvas = Figurecanvas(self)
        self.model = listmodel

        # set buttons
        self.redraw_button = QtWidgets.QPushButton(self)
        self.redraw_button.setObjectName("Redraw button")
        self.redraw_button.setText("Redraw")

        self.savefig_button = QtWidgets.QPushButton(self)
        self.savefig_button.setObjectName("Save Fig. button")
        self.savefig_button.setText("Save Fig As ...")

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

        # signal slot connection
        self.redraw_button.clicked.connect(self.redraw)
        self.savefig_button.clicked.connect(self.save_figure)
        self.quick_save_button.clicked.connect(self.quick_save_figure)
        self.xlim_min_box.textChanged.connect(self.redraw)
        self.xlim_max_box.textChanged.connect(self.redraw)

    def redraw(self):
        try:
            data = self.model.get_current_data()
        except NoSectionError as e:
            # if invalid section was selected, display the warning window.
            mes = e.args[0]
            QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                                          QtWidgets.QMessageBox.Ok)
            return

        self.figcanvas.set_xlim(self.xlim_min_box.text(), 
                                self.xlim_max_box.text())
        self.figcanvas.plot_fig(data)

    def save_figure(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", os.path.expanduser('~') + "/plot.png",
            filter="images (*.png *.jpg *.pdf)")
        file_save_to = filename[0]
        # if filename is empty string, do nothing
        if not file_save_to:
            return
        self.figcanvas.save_fig_to(file_save_to)

    def quick_save_figure(self):
        file_save_to = os.path.expanduser('~') + "/plot.png"
        self.figcanvas.save_fig_to(file_save_to)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = PlotArea()

    win.show()

    app.exec_()