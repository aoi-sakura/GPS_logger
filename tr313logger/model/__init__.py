#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Location(object):
    def __init__(
            self, imei, report_type, status, pend_column1,
            num_of_satellites, datetime, longitude, latitude, pend_column2,
            pend_column3, pend_column4, pend_column5, pend_column6,
            battery):
        self.seq_no = None
        self.imei = imei
        self.report_type = report_type
        self.status = status
        self.pend_column1 = pend_column1
        self.num_of_satellites = num_of_satellites
        self.datetime = datetime
        self.longitude = longitude
        self.latitude = latitude
        self.pend_column2 = pend_column2
        self.pend_column3 = pend_column3
        self.pend_column4 = pend_column4
        self.pend_column5 = pend_column5
        self.pend_column6 = pend_column6
        self.battery = battery
