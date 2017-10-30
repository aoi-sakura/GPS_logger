# -*- coding: utf-8 -*-

import logging
from contextlib import contextmanager
from tr313logger.repository import Session


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    https://stackoverflow.com/questions/14799189/avoiding-boilerplate-session-handling-code-in-sqlalchemy-functions
    """
    # http://d.hatena.ne.jp/heavenshell/20160220/1455987788
    # session = Session(expire_on_commit=False)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
