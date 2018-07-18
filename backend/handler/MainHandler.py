#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

from handler.BaseHandler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.http_header()
        self.json_response({
            "status": 200,
            "message": "hello world!",
        })
