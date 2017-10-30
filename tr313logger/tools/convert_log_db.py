#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
% convert_log_db sample_log.txt 'sqlite:///test.db'
"""

import sys
from tr313logger.repository import initialize as db_initialize, Session
from tr313logger.parser import gen_location_from_raw, validation


def usage():
    print("convert_command input_log_text output_sqlite_data\n")


def convert(input_filename):
    session = Session()

    with open(input_filename, mode='r', encoding='utf-8') as fd:
        for line in fd.readlines():
            line = line.strip()
            print(line)

            if validation(line):
                location = gen_location_from_raw(line)
                session.add(location)

        session.commit()


def main():
    input_file = None
    output_schema = None
    if len(sys.argv) != 3:
        usage()
    else:
        input_file = sys.argv[1]
        output_schema = sys.argv[2]

    db_initialize(output_schema)
    convert(input_file)


if __name__ == '__main__':
    main()
