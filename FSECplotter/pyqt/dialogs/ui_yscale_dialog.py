# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yscale_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_YaxisScalingDialog(object):
    def setupUi(self, YaxisScalingDialog):
        YaxisScalingDialog.setObjectName("YaxisScalingDialog")
        YaxisScalingDialog.resize(362, 179)
        self.verticalLayout = QtWidgets.QVBoxLayout(YaxisScalingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(YaxisScalingDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.x_axis_label = QtWidgets.QLabel(YaxisScalingDialog)
        self.x_axis_label.setObjectName("x_axis_label")
        self.horizontalLayout.addWidget(self.x_axis_label)
        self.lineEdit = QtWidgets.QLineEdit(YaxisScalingDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.unit_label = QtWidgets.QLabel(YaxisScalingDialog)
        self.unit_label.setObjectName("unit_label")
        self.horizontalLayout.addWidget(self.unit_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.x_axis_label_2 = QtWidgets.QLabel(YaxisScalingDialog)
        self.x_axis_label_2.setObjectName("x_axis_label_2")
        self.horizontalLayout_3.addWidget(self.x_axis_label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(YaxisScalingDialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.unit_label_2 = QtWidgets.QLabel(YaxisScalingDialog)
        self.unit_label_2.setObjectName("unit_label_2")
        self.horizontalLayout_3.addWidget(self.unit_label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(YaxisScalingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.x_axis_label.setBuddy(self.lineEdit)
        self.x_axis_label_2.setBuddy(self.lineEdit_2)

        self.retranslateUi(YaxisScalingDialog)
        self.buttonBox.accepted.connect(YaxisScalingDialog.accept)
        self.buttonBox.rejected.connect(YaxisScalingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(YaxisScalingDialog)

    def retranslateUi(self, YaxisScalingDialog):
        _translate = QtCore.QCoreApplication.translate
        YaxisScalingDialog.setWindowTitle(_translate("YaxisScalingDialog", "Y-axis Scaling"))
        self.label.setText(_translate("YaxisScalingDialog", "Normalize plots at the max value in the selected range."))
        self.x_axis_label.setText(_translate("YaxisScalingDialog", "Min. Volume"))
        self.unit_label.setText(_translate("YaxisScalingDialog", "(mL)"))
        self.x_axis_label_2.setText(_translate("YaxisScalingDialog", "Max. Volume"))
        self.unit_label_2.setText(_translate("YaxisScalingDialog", "(mL)"))

