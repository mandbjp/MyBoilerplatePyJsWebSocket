#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
import tornado.websocket
import json
import uuid


cone = []
cone_id = 0


class SocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, **kwargs):
        self.db = kwargs["database"]
        global cone_id
        self.cone_id = cone_id
        cone_id += 1

    def check_origin(self, origin):
        # @see http://www.tornadoweb.org/en/stable/websocket.html#configuration
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
            self.db.add_chat(payload["name"], payload["message"])
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
