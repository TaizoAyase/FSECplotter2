# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tmcalc_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TmCalcDialog(object):
    def setupUi(self, TmCalcDialog):
        TmCalcDialog.setObjectName("TmCalcDialog")
        TmCalcDialog.resize(312, 377)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(TmCalcDialog)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(TmCalcDialog)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(TmCalcDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(TmCalcDialog)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(TmCalcDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.label_2.setBuddy(self.lineEdit)
        self.label_3.setBuddy(self.lineEdit)
        self.label.setBuddy(self.comboBox)

        self.retranslateUi(TmCalcDialog)
        self.buttonBox.accepted.connect(TmCalcDialog.accept)
        self.buttonBox.rejected.connect(TmCalcDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TmCalcDialog)

    def retranslateUi(self, TmCalcDialog):
        _translate = QtCore.QCoreApplication.translate
        TmCalcDialog.setWindowTitle(_translate("TmCalcDialog", "Tm calculation"))
        self.label_4.setText(_translate("TmCalcDialog", "Temperature"))
        self.set_temp_button.setText(_translate("TmCalcDialog", "Set"))
        self.label_2.setText(_translate("TmCalcDialog", "Scale at"))
        self.label_3.setText(_translate("TmCalcDialog", "mL"))
        self.label.setText(_translate("TmCalcDialog", "Normalize with"))

