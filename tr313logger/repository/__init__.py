#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, BigInteger, String, DateTime,\
    Float, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker, scoped_session
from tr313logger.model import Location


# http://omake.accense.com/static/doc-ja/sqlalchemy/session.html#id24
Session = scoped_session(sessionmaker())
metadata = MetaData()

# auto_increment for sqlite3:
#   - http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
locations = Table('locations', metadata,
                  Column('seq_no', Integer, primary_key=True, autoincrement=True),
                  Column('imei', String),
                  Column('report_type', Integer),
                  Column('status', Integer),
                  Column('pend_column1', String),
                  Column('num_of_satellites', Integer),
                  Column('datetime', DateTime, index=True),
                  Column('longitude', Float),
                  Column('latitude', Float),
                  Column('pend_column2', String),
                  Column('pend_column3', String),
                  Column('pend_column4', String),
                  Column('pend_column5', String),
                  Column('pend_column6', String),
                  Column('battery', Integer),
                  sqlite_autoincrement=True
                  )

mapper(Location, locations)


def initialize(schema: str, echo=False):
    engine = create_engine(schema, echo=echo)
    metadata.create_all(engine)
    Session.configure(bind=engine)
