#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options
import urls
import db

define("port", default=8888, help="run on the given port", type=int)


store = db.Db()
store.connect()


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        urls.get_urls(database=store),
        debug=True,
    )

    print("server starting at PORT=%d" % options.port)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("exiting...")


if __name__ == "__main__":
    main()
