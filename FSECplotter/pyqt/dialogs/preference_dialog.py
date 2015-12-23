#!/usr/bin/env python
# -*- coding: utf-8 -*-

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



