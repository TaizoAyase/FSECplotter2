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

import numpy as np


def y_scale(model, min_vol, max_vol):
    # if the same values was selected for min/max,
    # add 0.1 to max to abort app. down
    if min_vol == max_vol:
        max_vol += 0.1

    # select enabled data
    data = model.get_current_data()
    data_ary = [d for d, f in zip(data['data'], data['enable_flags']) if f]

    # get nearest indices to the min/max value
    min_idx = [np.argmin(np.abs(d[:, 0] - min_vol)) for d in data_ary]
    max_idx = [np.argmin(np.abs(d[:, 0] - max_vol)) for d in data_ary]

    max_val_ary = [
        max(d[min_x:max_x, 1]) for min_x, max_x, d in zip(min_idx, max_idx, data_ary)
        ]

    norm_val = max(max_val_ary)
    scale_factor = max_val_ary / norm_val
    return scale_factor

