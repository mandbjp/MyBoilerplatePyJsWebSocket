#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.autoreload
from tornado.options import define, options

import json

import db
import uuid

define("port", default=8888, help="run on the given port", type=int)


cone = []
cone_id = 0

store = db.Db()


class BaseHandler(tornado.web.RequestHandler):
    def json_response(self, payload):
        self.add_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps(payload, indent=2))

    def http_header(self):
        self.add_header("Content-Type", "text/html; charset=utf-8")
        self.add_header("X-Content-Type-Options", "nosniff")


class MainHandler(BaseHandler):
    def get(self):
        self.http_header()
        self.json_response({
            "status": 200,
            "message": "hello world!",
        })


class ChatHistoryHandler(BaseHandler):
    def get(self):
        history = store.get_chats()
        self.http_header()
        self.json_response({
            "status": 200,
            "history": history,
        })


class SocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        global cone_id
        self.cone_id = cone_id
        cone_id += 1

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cone:
            cone.append(self)
        print("-------------------")
        print("connected")
        print(len(cone), self)
        print("--------------------")

    def on_close(self):
        if self in cone:
            cone.remove(self)
        print("------------------")
        print("dis-connected")
        print(len(cone), self)
        print("-------------------")

    def on_message(self, message):
        js = json.loads(message)
        print(self.cone_id, message)
        payload = js["payload"] if "payload" in js else None

        if js['command'] == 'PING':
            ret = {'command': 'PONG'}
            self.write_message(json.dumps(ret))
            return

        if js['command'] == 'TEXT_CHAT':
            store.add_chat(payload["name"], payload["message"])
            for c in cone:
                if c is self:
                    continue
                c.send_command('TEXT_CHAT', payload)
            return

        if js['command'] == 'IINE':
            for c in cone:
                if c is self:
                    continue
                c.send_command('IINE', payload)
            return

        if js['command'] == 'GIVE-ME-NAME':
            name = uuid.uuid4().hex
            print("your name is {}".format(name))
            self.send_command(js["command"], {"name": name})
            return

    def send_command(self, command, payload):
        self.write_message(json.dumps({
            "command": command,
            "payload": payload,
        }))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/api/greet", MainHandler),
            (r"/api/history", ChatHistoryHandler),
            (r"/websocket", SocketHandler),
        ],
        debug=True,

    )

    print("server starting at PORT=%d" % options.port)

    store.connect()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("exiting...")


if __name__ == "__main__":
    main()
