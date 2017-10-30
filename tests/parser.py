#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
% nosetests tests/parser.py
"""

from nose.tools import with_setup, raises
from tr313logger import parser


def test_gen_location_01():
    raw = "GSr,703395238346751,1,3,00,,5,151021,200433,E13831.3821,N3613.4411,0,0.00,0,1,0.0,91*4b!"
    location = parser.gen_location_from_raw(raw)

    assert location.longitude == 138.523035
    assert location.latitude == 36.22401833333333
    assert location.battery == '91'
