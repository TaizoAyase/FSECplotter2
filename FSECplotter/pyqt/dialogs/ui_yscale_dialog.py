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
        YaxisScalingDialog.resize(480, 187)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(YaxisScalingDialog)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.filename_label = QtWidgets.QLabel(YaxisScalingDialog)
        self.filename_label.setObjectName("filename_label")
        self.horizontalLayout_2.addWidget(self.filename_label)
        self.filename_for_normal = QtWidgets.QComboBox(YaxisScalingDialog)
        self.filename_for_normal.setObjectName("filename_for_normal")
        self.horizontalLayout_2.addWidget(self.filename_for_normal)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(YaxisScalingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(YaxisScalingDialog)
        self.buttonBox.accepted.connect(YaxisScalingDialog.accept)
        self.buttonBox.rejected.connect(YaxisScalingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(YaxisScalingDialog)

    def retranslateUi(self, YaxisScalingDialog):
        _translate = QtCore.QCoreApplication.translate
        YaxisScalingDialog.setWindowTitle(_translate("YaxisScalingDialog", "Y-axis Scaling"))
        self.x_axis_label.setText(_translate("YaxisScalingDialog", "Scaling at "))
        self.unit_label.setText(_translate("YaxisScalingDialog", "(mL)"))
        self.filename_label.setText(_translate("YaxisScalingDialog", "File used as Normal"))

