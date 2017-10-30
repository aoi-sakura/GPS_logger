#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
% logger_client [host:port] [data]
"""

import argparse
import socket


def send_data(option):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((option.host, option.port))
        sock.send(option.data.encode('ascii'))
        print("finish.")
    except Exception as e:
        print(e)


def gen_defaults():
    return {
        'description': 'send packet to logger server for test.',
        'data': 'GSr,703395238346751,1,3,00,,5,151021,200433,E13831.3821,N3613.4411,0,0.00,0,1,0.0,91*4b!',
        'host': 'localhost',
        'port': 5000}


def gen_option_parser(default_options):
    parser = argparse.ArgumentParser(description=default_options['description'])
    parser.add_argument('-H', '--host', dest='host', default=default_options['host'],
                        help='target server hostname [default: %s]' % default_options['host'])
    parser.add_argument('-p', '--port', dest='port', default=default_options['port'],
                        help='target server port [default: %d]' % default_options['port'])
    parser.add_argument('data', nargs='?', default=default_options['data'],
                        help='default data')
    return parser


def main():
    defaults = gen_defaults()
    opt_parser = gen_option_parser(defaults)
    args = opt_parser.parse_args()
    send_data(args)


if __name__ == '__main__':
    main()
