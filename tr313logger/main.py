# -*- coding: utf-8 -*-

import logging
import os
import json
import tornado.web
import argparse
import tornado.process
from tornado import gen
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
from tornado.tcpserver import TCPServer
from datetime import datetime

from tr313logger import DATE_FORMAT
from tr313logger.config import configure
from tr313logger.repository import initialize as db_initialize
from tr313logger.logic import get_latest_point, get_latest_points, register_location
from tr313logger.parser import gen_location_from_raw, validation

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "cookie_secret": None,
    "xsrf_cookies": True,
    "__googlemap_key": None
}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', googlemap_key=settings['__googlemap_key'])


class JSONHandler(tornado.web.RequestHandler):
    def get(self, subpath):
        # print("subpath: %s" % repr(subpath))
        if subpath == '':
            self.__get_index()
        elif subpath == 'latest':
            self.__get_latest()

    def __get_latest(self):
        location = get_latest_point()
        self.write(location)

    def __get_index(self):
        from_date = self.get_argument('from_date', '2017/09/24 00:00:00')
        to_date = self.get_argument('to_date', '2017/09/25 00:00:00')

        locations = None
        try:
            start = datetime.strptime(from_date, DATE_FORMAT)
            end = datetime.strptime(to_date, DATE_FORMAT)
            locations = get_latest_points(start, end)
        except ValueError:
            print("invalid format: " + from_date + ', ' + to_date)

        # jsonized = json.dumps(locations, ensure_ascii=False)
        self.write(locations)


class LoggerServer(TCPServer):
    """
    Server for logger to reveive request location data.
    """
    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                request = yield stream.read_until_close()
                if not request:
                    break

                logger.info(request)
            except Exception as e:
                logger.error(e)
                break
            data = request.decode('utf-8', "backslashreplace")

            if validation(data):
                location = gen_location_from_raw(data.strip())
                register_location(location)
            else:
                logger.warning("error: %s %s\n" % (address, data))


def init(schema: str):
    db_initialize(schema, echo=True)


def get_parser():
    parser = argparse.ArgumentParser(description='logger and viewer server.')
    parser.add_argument('-c', '--config', dest='config_path', metavar='config_path',
                        type=str, required=True,
                        help='configuration file path')
    return parser


if __name__ == '__main__':
    opt_parser = get_parser()
    config = configure(opt_parser.parse_args().config_path)

    init(config['app:main']['sqlalchemy.url'])

    web_sockets = bind_sockets(config['app:web']['port'])
    logger_sockets = bind_sockets(config['app:logger']['port'])
    # MEMO: bind_sockets は↓の前に必ず実行する
    tornado.process.fork_processes(0)

    settings['cookie_secret'] = config['app:web']['cookie_secret']
    # TODO: global variable access
    settings['__googlemap_key'] = config['app:web']['googlemap_key']

    web_app = tornado.web.Application(handlers=[(r'/', IndexHandler), ('/json/(.*)', JSONHandler)], **settings)
    web_server = HTTPServer(web_app)
    web_server.add_sockets(web_sockets)

    logger_server = LoggerServer()
    logger_server.add_sockets(logger_sockets)

    tornado.ioloop.IOLoop.current().start()
