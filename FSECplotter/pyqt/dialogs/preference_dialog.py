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
from FSECplotter.pyqt.dialogs.ui_preference_dialog import Ui_PreferenceDialog

DEFAULT_PARAMETERS = [
    'detector',
    'channel',
    'flowrate',
    'linewidth',
    'ts_gain',
    'ts_tm'
]

class PreferenceDialog(QtWidgets.QDialog):

    def __init__(self, restored, parent=None):
        super().__init__(parent)
        self.ui = Ui_PreferenceDialog()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        valid = QtGui.QDoubleValidator()
        self.ui.ts_gain_lineEdit.setValidator(valid)
        self.ui.ts_tm_lineEdit.setValidator(valid)

        self.set_params(restored)

    def set_params(self, params):
        self.ui.detector_comboBox.setCurrentIndex(int(params['detector']))
        self.ui.channel_spinBox.setValue(int(params['channel']))
        self.ui.flowrate_spinBox.setValue(float(params['flowrate']))
        self.ui.linewidth_spinBox.setValue(float(params['linewidth']))
        self.ui.ts_gain_lineEdit.setText(str(params['ts_gain']))
        self.ui.ts_tm_lineEdit.setText(str(params['ts_tm']))


    def get_params(self):
        params = {}
        params['detector'] = self.ui.detector_comboBox.currentIndex()
        params['channel'] = self.ui.channel_spinBox.value()
        params['flowrate'] = self.ui.flowrate_spinBox.value()
        params['linewidth'] = self.ui.linewidth_spinBox.value()
        params['ts_gain'] = self.ui.ts_gain_lineEdit.text()
        params['ts_tm'] = self.ui.ts_tm_lineEdit.text()
        return params



