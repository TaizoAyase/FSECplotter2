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
        YaxisScalingDialog.resize(286, 99)
        
        self.verticalLayoutWidget = QtWidgets.QWidget(YaxisScalingDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 1, 249, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.x_axis_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.x_axis_label.setObjectName("x_axis_label")
        self.horizontalLayout.addWidget(self.x_axis_label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.unit_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.unit_label.setObjectName("unit_label")
        self.horizontalLayout.addWidget(self.unit_label)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(YaxisScalingDialog)
        self.buttonBox.accepted.connect(YaxisScalingDialog.accept)
        self.buttonBox.rejected.connect(YaxisScalingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(YaxisScalingDialog)

    def retranslateUi(self, YaxisScalingDialog):
        _translate = QtCore.QCoreApplication.translate
        YaxisScalingDialog.setWindowTitle(_translate(
            "YaxisScalingDialog", "Y-axis Scaling"))
        self.x_axis_label.setText(_translate(
            "YaxisScalingDialog", "Scaling at "))
        self.unit_label.setText(_translate(
            "YaxisScalingDialog", "(mL)"))

