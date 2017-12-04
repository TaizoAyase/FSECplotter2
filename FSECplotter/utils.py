#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FSECplotter2 - The interactive plotting application for FSEC.

Copyright 2015-2017, TaizoAyase, tikuta, biochem-fan

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

import numpy as np


def calc_yscale_factor(model, min_vol, max_vol):
    # if the same values was selected for min/max,
    # add 0.1 to max to abort app. down
    if min_vol == max_vol:
        max_vol += 0.1

    # select enabled data
    data = model.get_current_data()
    data_ary = [d for d, f in zip(data['data'], data['enable_flags']) if f]
    num_data = len(data['filenames'])

    # convert x-axis value to volume
    for i in range(num_data):
        x = data['data'][i][:, 0]
        x *= data['flowrate'][i]

    # get nearest indices to the min/max value
    min_idx = [np.argmin(np.abs(d[:, 0] - min_vol)) for d in data_ary]
    max_idx = [np.argmin(np.abs(d[:, 0] - max_vol)) for d in data_ary]

    max_val_ary = [
        max(d[min_x:max_x, 1]) for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
        ]

    norm_val = max(max_val_ary)
    scale_factor = max_val_ary / norm_val
    return scale_factor


def calc_peak(model, min_vol, max_vol):
    data = model.get_current_data()
    flags = data['enable_flags']

    data_ary = [d for d, f in zip(data['data'], flags) if f]
    num_data = len(data['filenames'])

    filenames = [f for f, fl in zip(data['filenames'], flags) if fl]

    for i in range(num_data):
        x = data['data'][i][:, 0]
        x *= data['flowrate'][i]

    min_idx = [np.argmin(np.abs(d[:, 0] - min_vol)) for d in data_ary]
    max_idx = [np.argmin(np.abs(d[:, 0] - max_vol)) for d in data_ary]

    max_vol_idx = [
        np.argmax(d[min_x:max_x, 1]) for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
    ]
    max_vol_ary = [
        d[idx, 0] + min_vol for idx, d in zip(max_vol_idx, data_ary)
    ]

    max_val_ary = [
        max(d[min_x:max_x, 1]) for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
    ]

    return filenames, max_vol_ary, max_val_ary


def get_enabled_filename(model):
    data = model.get_current_data()
    ary = []
    for f, flag in zip(data['filenames'], data['enable_flags']):
        if not flag:
            continue
        ary.append(f)

    del data
    return ary


def peak_integrate(model, min_vol, max_vol):
    # select enebled data
    data = model.get_current_data()
    data_ary = [d for d, f in zip(data['data'], data['enable_flags']) if f]
    num_data = len(data['filenames'])

    # convert x-axis value to volume
    for i in range(num_data):
        x = data['data'][i][:, 0]
        x *= data['flowrate'][i]

    # get nearest indices to the min/max value
    min_idx = [np.argmin(np.abs(d[:, 0] - min_vol)) for d in data_ary]
    max_idx = [np.argmin(np.abs(d[:, 0] - max_vol)) for d in data_ary]

    delx_val_ary = [
        d[min_x+1:max_x+1, 0] - d[min_x:max_x, 0] for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
    ]
    y_val_ary = [
        d[min_x:max_x, 1] for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
    ]

    # sum over the product of (delta * y) for each data
    prod_val = [
        sum(delta * val) for delta, val in zip(delx_val_ary, y_val_ary)
    ]

    return prod_val
