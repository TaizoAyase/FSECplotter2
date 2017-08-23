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
from FSECplotter.core.factory import LogfileFactory
from FSECplotter.core.shimadzu import NoSectionError, NoMatchedFlowRateError
import os
import string

# list background color
COLOR_LIST = [
    QtGui.QBrush(QtGui.QColor(255, 255, 255)),
    QtGui.QBrush(QtGui.QColor(240, 240, 240))
]


class LogfileModel(QtGui.QStandardItemModel):
    """ The class that has logfile-ary.
        Also this is a model for ListView. """

    # override itemChanged signal
    itemChanged = QtCore.pyqtSignal()

    def __init__(self, row, col, parent=None):
        super(LogfileModel, self).__init__(row, col, parent)
        self.logfiles = {}
        self.logfile_factory = LogfileFactory()
        self.__id_count = 1

        # set header data
        self.headers = ('Id', 'Filename', 'Flow rate(ml/min)',
                        'Detector', 'Channel', 'Color')
        for i, item in enumerate(self.headers):
            self.setHeaderData(i, QtCore.Qt.Horizontal, item)

        self.current_dir = os.path.expanduser("~")

        # signal - slot connection
        self.itemChanged.connect(self.__update_background_color)

        # default parameters
        self.def_detector = "B"
        self.def_channel = 1
        self.def_flowrate = 1.0

    def updateDefaultParameters(self, **kwargs):
        self.def_detector = string.ascii_uppercase[ int(kwargs['detector']) ]
        self.def_channel = int(kwargs['channel'])
        self.def_flowrate = float(kwargs['flowrate'])

    def add_item(self, filename):
        abspath = os.path.abspath(filename)
        new_log = self.__append_logfile(abspath)
        warning_dialog_flag = False

        if new_log.num_detectors == 2:
            default_detector = self.def_detector 
        else:
            default_detector = "A"

        if new_log.flowrate is None:
            warning_dialog_flag = True
            new_log.flowrate = self.def_flowrate

        default_channel = self.def_channel
        default_color = 'Default'

        row = self.rowCount()
        order = self.__id_count
        self.__id_count += 1
        data_ary = [order,
                    new_log.filename,
                    new_log.flowrate,
                    default_detector,
                    default_channel,
                    default_color]

        for i in range(len(data_ary)):
            # create new Item and set texts in data_ary
            item = QtGui.QStandardItem()
            if i == 0:
                item.setCheckable(True)
                item.setCheckState(2)  # take value of 0, 1 or 2
            elif i == 5:
                item.setEditable(False)
            item.setText(str(data_ary[i]))
            item.setBackground(COLOR_LIST[row % 2])

            # test for nested-tree object
            # tmp = QtGui.QStandardItem('hogehoge')
            # item.appendRow(tmp)

            self.setItem(row, i, item)

        self.itemChanged.emit()
        self.current_dir = os.path.dirname(abspath)

        if warning_dialog_flag:
            mes = ('''\
The input file '%s' doesn't contain the flow rate information.\
Flow rate will be set %.2f ml/min.''' % (abspath, self.def_flowrate)).strip()
            raise NoMatchedFlowRateError(mes)


    def move_item(self, current_index, shift):
        next_row_num = current_index + int(shift)

        # if the top or bottom item is selected, beep and ignore
        if next_row_num < 0 or next_row_num == self.rowCount():
            QtWidgets.QApplication.beep()
            return current_index

        # pop the row and insert to new position
        target_row = self.takeRow(current_index)
        self.insertRow(next_row_num, target_row)

        self.itemChanged.emit()

        return next_row_num

    def delete_item(self, row_num):
        # We also remove the item from logfile array
        target_row = self.takeRow(row_num)
        del_id = target_row[0].text()
        del_logfile = self.logfiles.pop(int(del_id))
        del target_row
        del del_logfile

        self.itemChanged.emit()

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()  # create Mime Data
        urllist = []
        for index in indexes:
            # if the index of column is 0, do nothing
            if index.column() != 0:
                continue

            item = self.itemFromIndex(index)
            filepath = item.text()

            # windows requires "/" in top
            # this not affect unix env.
            # and the urllist require the QUrl obj.,
            # cast the string to QUrl
            urllist.append(QtCore.QUrl('/' + filepath))
        mimedata.setUrls(urllist)

        return mimedata

    def get_current_data(self):
        data = {}
        data['total_data'] = self.rowCount()
        data['filenames'] = []
        data['flowrate'] = []
        data['data'] = []
        data['enable_flags'] = []
        data['color'] = []

        for i in range(self.rowCount()):
            enable = self.item(i, 0).checkState() == 2
            data['enable_flags'].append(enable)

            log_id = int(self.item(i, 0).text())

            detector = self.item(i, 3).text()
            channel_no = int(self.item(i, 4).text())

            # set data ary
            filename = self.item(i, 1).text()
            kwargs = {'detector': detector, 'channel': channel_no}
            try:
                data_table = self.logfiles[log_id].data(**kwargs)
            except NoSectionError:
                mes = ("""\
In the file '%s', Detector '%s' and Channel '%s' is not exist.\
""" % (filename, detector, channel_no)).strip()
                raise NoSectionError(mes)

            flowrate = float(self.item(i, 2).text())
            d = data_table.copy()
            #d[:, 0] = data_table[:, 0] * flowrate
            
            data['data'].append(d)
            data['filenames'].append(filename)
            data['flowrate'].append(flowrate)

            # set color
            col = self.item(i, 5).text()
            data['color'].append(None if col == "Default" else str(col))

        return data

    def get_color(self, row):
        return str(self.item(row, 5))

    def set_color(self, row, color):
        self.item(row, 5).setText(color)
        self.itemChanged.emit()

    def reset_color(self, row):
        self.item(row, 5).setText('Default')
        self.itemChanged.emit()

    def change_all_check_state(self, check_state):
        for i in range(self.rowCount()):
            checkable_item = self.item(i, 0)
            checkable_item.setCheckState(check_state)

    def select_params_to(self, col, param):
        for i in range(self.rowCount()):
            item = self.item(i, col)
            item.setText(param)
        self.itemChanged.emit()

    def save_csv_table(self, filename):
        # save current data table with long format dataframe
        data = self.get_current_data()
        n_enabled_data = sum(data['enable_flags'])
        csv_string = "Volume, Intensity, filename\n"
        for i in range(n_enabled_data):
            d = data['data'][i]
            data_len = d.shape[0]
            for j in range(data_len):
                fname = data['filenames'][i]
                csv_string += "%f, %f, %s\n" % (d[j, 0], d[j, 1], fname)

        with open(filename, 'w+') as f:
            f.write(csv_string)

    # private methods

    def __append_logfile(self, filepath):
        try:
            logfile = self.logfile_factory.create(filepath)
        except NoSectionError:
            #logfile.flowrate = self.flowrate
            mes = ("""\
The input file '%s' lacks some required section. Skipped.\
                """ % filepath).strip()
            raise NoSectionError(mes)

        self.logfiles[self.__id_count] = logfile
        return logfile

    def __update_background_color(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                # color field is colored with the user color
                if col == 5 and item.text() != 'Default':
                    color = QtGui.QColor(item.text())
                    item.setBackground(color)
                else:
                    item.setBackground(COLOR_LIST[row % 2])

