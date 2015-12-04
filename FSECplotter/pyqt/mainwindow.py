#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.centralWidget = QtWidgets.QWidget(self)

        # set list view and plot widgets
        self.treeview = LogfileListWidget(self)
        self.plotarea = PlotArea(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.addWidget(self.treeview)
        self.horizontalLayout.addWidget(self.plotarea)

        self.setCentralWidget(self.centralWidget)

        self.resize(1200, 600)
        self.setWindowTitle("FSEC plotter 2")

        # signal slot definition
        self.plotarea.redraw_button.clicked.connect(self.redraw)
        self.plotarea.savefig_button.clicked.connect(self.save_figure)
        self.plotarea.quick_save_button.clicked.connect(self.quick_save_figure)

        # make first plot
        #self.redraw()

    def redraw(self):
        try:
            data = self.treeview.model.get_current_data()
        except NoSectionError as e:
            # if invalid section was selected, display the warning window.
            mes = e.args[0]
            QtWidgets.QMessageBox.warning(self, "FSEC plotter 2", mes,
                                          QtWidgets.QMessageBox.Ok)
            return

        x_min, x_max = self.figcanvas.set_xlim(
            self.xlim_min_box.text(), self.xlim_max_box.text())
        self.xlim_min_box.setText(str(x_min))
        self.xlim_max_box.setText(str(x_max))
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

    win = MainWindow()
    win.show()

    app.exec_()
