#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

from handler.BaseHandler import BaseHandler


class ChatHistoryHandler(BaseHandler):
    def initialize(self, **kwargs):
        self.db = kwargs["database"]

    def get(self):
        history = self.db.get_chats()
        self.http_header()
        self.json_response({
            "status": 200,
            "history": history,
        })
