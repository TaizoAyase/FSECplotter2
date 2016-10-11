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

# Form implementation generated from reading ui file 'peaktable_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PeakTableDialog(object):
    def setupUi(self, PeakTableDialog):
        PeakTableDialog.setObjectName("PeakTableDialog")
        PeakTableDialog.resize(463, 545)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(PeakTableDialog)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(PeakTableDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(PeakTableDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_min = QtWidgets.QLineEdit(PeakTableDialog)
        self.lineEdit_min.setObjectName("lineEdit_min")
        self.horizontalLayout.addWidget(self.lineEdit_min)
        self.label_3 = QtWidgets.QLabel(PeakTableDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(PeakTableDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_max = QtWidgets.QLineEdit(PeakTableDialog)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.horizontalLayout_2.addWidget(self.lineEdit_max)
        self.label_4 = QtWidgets.QLabel(PeakTableDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.normalizeCheckBox = QtWidgets.QCheckBox(PeakTableDialog)
        self.normalizeCheckBox.setObjectName("normalizeCheckBox")
        self.verticalLayout.addWidget(self.normalizeCheckBox)
        self.tableWidget = QtWidgets.QTableWidget(PeakTableDialog)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.updateButton = QtWidgets.QPushButton(PeakTableDialog)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_3.addWidget(self.updateButton)
        self.saveCSVButton = QtWidgets.QPushButton(PeakTableDialog)
        self.saveCSVButton.setObjectName("saveCSVButton")
        self.horizontalLayout_3.addWidget(self.saveCSVButton)
        self.okButton = QtWidgets.QPushButton(PeakTableDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_3.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.label.setBuddy(self.lineEdit_min)
        self.label_3.setBuddy(self.lineEdit_min)
        self.label_2.setBuddy(self.lineEdit_max)
        self.label_4.setBuddy(self.lineEdit_max)

        self.retranslateUi(PeakTableDialog)
        QtCore.QMetaObject.connectSlotsByName(PeakTableDialog)
        PeakTableDialog.setTabOrder(self.lineEdit_min, self.lineEdit_max)
        PeakTableDialog.setTabOrder(self.lineEdit_max, self.tableWidget)
        PeakTableDialog.setTabOrder(self.tableWidget, self.updateButton)
        PeakTableDialog.setTabOrder(self.updateButton, self.saveCSVButton)
        PeakTableDialog.setTabOrder(self.saveCSVButton, self.okButton)

    def retranslateUi(self, PeakTableDialog):
        _translate = QtCore.QCoreApplication.translate
        PeakTableDialog.setWindowTitle(_translate("PeakTableDialog", "Peak table"))
        self.label_5.setText(_translate("PeakTableDialog", "Enter the range of volume in mL."))
        self.label.setText(_translate("PeakTableDialog", "Min. Volume "))
        self.label_3.setText(_translate("PeakTableDialog", "(mL)"))
        self.label_2.setText(_translate("PeakTableDialog", "Max. Volume"))
        self.label_4.setText(_translate("PeakTableDialog", "(mL)"))
        self.normalizeCheckBox.setText(_translate("PeakTableDialog", "Normalize with max value"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("PeakTableDialog", "Filename"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("PeakTableDialog", "Volume(ml)"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("PeakTableDialog", "Max peak(A.U.)"))
        self.updateButton.setText(_translate("PeakTableDialog", "Update"))
        self.saveCSVButton.setText(_translate("PeakTableDialog", "Save CSV"))
        self.okButton.setText(_translate("PeakTableDialog", "OK"))

