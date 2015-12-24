#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                        'Detector', 'Channel')
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
        self.flowrate = float(kwargs['flowrate'])

    def add_item(self, filename):
        abspath = os.path.abspath(filename)
        new_log = self.__append_logfile(abspath)

        if new_log.num_detectors == 2:
            default_detector = self.def_detector 
        else:
            default_detector = "A"

        default_channel = self.def_channel

        row = self.rowCount()
        order = self.__id_count
        self.__id_count += 1
        data_ary = [order,
                    new_log.filename,
                    new_log.flowrate,
                    default_detector,
                    default_channel]

        for i in range(len(data_ary)):
            # create new Item and set texts in data_ary
            item = QtGui.QStandardItem()
            if i == 0:
                item.setCheckable(True)
                item.setCheckState(2)  # take value of 0, 1 or 2
            item.setText(str(data_ary[i]))
            item.setBackground(COLOR_LIST[row % 2])

            self.setItem(row, i, item)

        self.itemChanged.emit()
        self.current_dir = os.path.dirname(abspath)

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
                In the file '%s', Detector '%s' and\
                Channel '%s' is not exist.""" % (
                    filename, detector, channel_no)).strip()
                raise NoSectionError(mes)

            flowrate = float(self.item(i, 2).text())
            d = data_table.copy()
            d[:, 0] = data_table[:, 0] * flowrate
            
            data['data'].append(d)
            data['filenames'].append(filename)
            data['flowrate'].append(self.item(i, 2).text())

        return data

    def change_all_check_state(self, check_state):
        for i in range(self.rowCount()):
            checkable_item = self.item(i, 0)
            checkable_item.setCheckState(check_state)

    def select_params_to(self, col, param):
        for i in range(self.rowCount()):
            item = self.item(i, col)
            item.setText(param)
        self.itemChanged.emit()

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
                item.setBackground(COLOR_LIST[row % 2])
