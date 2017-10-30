#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tr313logger.lib.format import TokyoDatetime, dmm_to_deg
from tr313logger.model import Location

tokyoDatetime = TokyoDatetime()


def validation(raw_record: str):
    return raw_record[:3] == 'GSr'


def gen_location_from_raw(raw_record: str):
    columns = raw_record.split(',')

    # 想定する並び順
    # ('GSr')
    # imei, report_type, status, pend_column1, "",
    # num_of_satellite, date, time, longitude_str, latitude_str,
    # pend_column2, pend_column3, pend_column4, pend_column5,
    # pend_column6, battery('*' 前)
    # (terminator ('*' 後))

    # ToDo: validation

    date = columns[7]
    time = columns[8]
    longitude_str = columns[9]
    latitude_str = columns[10]
    battery_str = columns[16]

    # UTC -> JST
    datetime = tokyoDatetime.from_str(date, time)

    # 頭文字に E or W が入っているのを想定
    longitude = dmm_to_deg(longitude_str[1:])
    if longitude_str[0] == 'W':
        longitude = longitude * -1
    elif longitude_str[0] != 'E':
        # ToDo: 想定した文字でないなら Error
        pass

    # 頭文字に N or S が入っているのを想定
    latitude = dmm_to_deg(latitude_str[1:])
    if latitude_str[0] == 'S':
        latitude = latitude * -1
    elif latitude_str[0] != 'N':
        # ToDo: 想定した文字でないなら Error
        pass

    battery = battery_str.split('*')[0]

    return Location(
        columns[1], columns[2], columns[3], columns[4],
        columns[6], datetime, longitude, latitude,
        columns[11], columns[12], columns[13], columns[14],
        columns[15], battery)
