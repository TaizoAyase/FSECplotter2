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

# Form implementation generated from reading ui file 'tmcalc_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TmCalcDialog(object):
    def setupUi(self, TmCalcDialog):
        TmCalcDialog.setObjectName("TmCalcDialog")
        TmCalcDialog.resize(347, 487)
        self.verticalLayout = QtWidgets.QVBoxLayout(TmCalcDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(TmCalcDialog)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.label_7 = QtWidgets.QLabel(TmCalcDialog)
        self.label_7.setScaledContents(False)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(TmCalcDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_temp = QtWidgets.QLineEdit(TmCalcDialog)
        self.lineEdit_temp.setObjectName("lineEdit_temp")
        self.horizontalLayout_4.addWidget(self.lineEdit_temp)
        self.set_temp_button = QtWidgets.QPushButton(TmCalcDialog)
        self.set_temp_button.setObjectName("set_temp_button")
        self.horizontalLayout_4.addWidget(self.set_temp_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(TmCalcDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(TmCalcDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(TmCalcDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(TmCalcDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(TmCalcDialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(TmCalcDialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.label_6 = QtWidgets.QLabel(TmCalcDialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(TmCalcDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.raise_()
        self.label_7.raise_()
        self.lineEdit_temp.raise_()
        self.label_2.setBuddy(self.lineEdit)
        self.label_3.setBuddy(self.lineEdit)
        self.label_5.setBuddy(self.lineEdit)
        self.label_6.setBuddy(self.lineEdit)

        self.retranslateUi(TmCalcDialog)
        self.buttonBox.accepted.connect(TmCalcDialog.accept)
        self.buttonBox.rejected.connect(TmCalcDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TmCalcDialog)

    def retranslateUi(self, TmCalcDialog):
        _translate = QtCore.QCoreApplication.translate
        TmCalcDialog.setWindowTitle(_translate("TmCalcDialog", "Tm calculation"))
        self.label_7.setText(_translate("TmCalcDialog", "Select the file, enter the temperature, and click set button."))
        self.label_4.setText(_translate("TmCalcDialog", "Temperature"))
        self.set_temp_button.setText(_translate("TmCalcDialog", "Set"))
        self.label.setText(_translate("TmCalcDialog", "Enter the min/max value for scaling."))
        self.label_2.setText(_translate("TmCalcDialog", "Min. volume"))
        self.label_3.setText(_translate("TmCalcDialog", "mL"))
        self.label_5.setText(_translate("TmCalcDialog", "Max volume"))
        self.label_6.setText(_translate("TmCalcDialog", "mL"))

