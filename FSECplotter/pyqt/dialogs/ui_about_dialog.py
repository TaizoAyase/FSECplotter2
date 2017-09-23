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

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(350, 151)
        self.horizontalLayout = QtWidgets.QHBoxLayout(AboutDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelAppName = QtWidgets.QLabel(AboutDialog)
        self.labelAppName.setTextFormat(QtCore.Qt.RichText)
        self.labelAppName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAppName.setObjectName("labelAppName")
        self.verticalLayout.addWidget(self.labelAppName)
        self.labelVersion = QtWidgets.QLabel(AboutDialog)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout.addWidget(self.labelVersion)
        self.labelBodyText = QtWidgets.QLabel(AboutDialog)
        self.labelBodyText.setOpenExternalLinks(True)
        self.labelBodyText.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.labelBodyText.setObjectName("labelBodyText")
        self.verticalLayout.addWidget(self.labelBodyText)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Dialog"))
        self.labelAppName.setText(_translate("AboutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">FSECplotter2</span></p></body></html>"))
        self.labelVersion.setText(_translate("AboutDialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt;\">version XXX</span></p></body></html>"))
        self.labelBodyText.setText(_translate("AboutDialog", "<html><head/><body><p>Developed by @Taizo_Ayase 2015-2017</p><p>Github: <a href=\"https://github.com/TaizoAyase/FSECplotter2\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/TaizoAyase/FSECplotter2</span></a></p></body></html>"))

