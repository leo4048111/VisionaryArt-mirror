#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
from functools import wraps

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import urls_tornado

import os
import mimetypes

mimetypes.init([r'./mime.types'])

static_handlers = [(r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "dist")}),]

settings = {
    'debug': False
}

define("port", default=7650, help="run on the given port", type=int)

class url_route(object):
    '''
    tornado url class
    '''

    def __init__(self):
        self.url_config = urls_tornado.urls
        self.route_tables = []

    def _import_handle(self, handle_path):
        '''
        import handles
        '''
        mod, cls = handle_path.rsplit('.', 1)
        mod = __import__(mod, {}, {}, [''])
        cls = getattr(mod, cls)
        return cls

    def _generate_handle_table(self):
        '''
        assemble the routes in the route table
        '''
        for item in self.url_config:
            # try:
            if 1:
                new_url = (item[0], self._import_handle(item[1]))
                self.route_tables.append((new_url))
            try:
                pass
            except Exception as e:
                print("url_import error:{}".format(e))

        for sh in static_handlers:
            self.route_tables.append(sh)

    def get_all_route(self):
        '''
        route table
        '''
        self._generate_handle_table()
        print(self.route_tables,)
        return self.route_tables


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)

    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)
options.parse_command_line()
application = tornado.web.Application(url_route().get_all_route(), **settings)

if __name__ == '__main__':
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
