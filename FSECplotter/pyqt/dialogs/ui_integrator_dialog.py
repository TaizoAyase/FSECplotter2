# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'integrator_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IntegratorDialog(object):
    def setupUi(self, IntegratorDialog):
        IntegratorDialog.setObjectName("IntegratorDialog")
        IntegratorDialog.resize(394, 179)
        self.verticalLayout = QtWidgets.QVBoxLayout(IntegratorDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(IntegratorDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.x_axis_label = QtWidgets.QLabel(IntegratorDialog)
        self.x_axis_label.setObjectName("x_axis_label")
        self.horizontalLayout.addWidget(self.x_axis_label)
        self.lineEdit = QtWidgets.QLineEdit(IntegratorDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.unit_label = QtWidgets.QLabel(IntegratorDialog)
        self.unit_label.setObjectName("unit_label")
        self.horizontalLayout.addWidget(self.unit_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.x_axis_label_2 = QtWidgets.QLabel(IntegratorDialog)
        self.x_axis_label_2.setObjectName("x_axis_label_2")
        self.horizontalLayout_3.addWidget(self.x_axis_label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(IntegratorDialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.unit_label_2 = QtWidgets.QLabel(IntegratorDialog)
        self.unit_label_2.setObjectName("unit_label_2")
        self.horizontalLayout_3.addWidget(self.unit_label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(IntegratorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.x_axis_label.setBuddy(self.lineEdit)
        self.x_axis_label_2.setBuddy(self.lineEdit_2)

        self.retranslateUi(IntegratorDialog)
        self.buttonBox.accepted.connect(IntegratorDialog.accept)
        self.buttonBox.rejected.connect(IntegratorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IntegratorDialog)

    def retranslateUi(self, IntegratorDialog):
        _translate = QtCore.QCoreApplication.translate
        IntegratorDialog.setWindowTitle(_translate("IntegratorDialog", "Integrate"))
        self.label.setText(_translate("IntegratorDialog", "Select the lower and upper range for using peak integration."))
        self.x_axis_label.setText(_translate("IntegratorDialog", "Min. Volume"))
        self.unit_label.setText(_translate("IntegratorDialog", "(mL)"))
        self.x_axis_label_2.setText(_translate("IntegratorDialog", "Max. Volume"))
        self.unit_label_2.setText(_translate("IntegratorDialog", "(mL)"))

