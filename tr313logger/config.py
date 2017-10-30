# -*- coding: utf-8 -*-

import configparser


def configure(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    return config
