#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    def json_response(self, payload):
        self.add_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps(payload, indent=2))

    def http_header(self):
        self.add_header("Content-Type", "text/html; charset=utf-8")
        self.add_header("X-Content-Type-Options", "nosniff")
