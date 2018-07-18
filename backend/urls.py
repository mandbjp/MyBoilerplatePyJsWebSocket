#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

from handler.MainHandler import MainHandler
from handler.ChatHistoryHandler import ChatHistoryHandler
from handler.SocketHandler import SocketHandler


def get_urls(**kwargs):
    return [
        # (url_pattern, handler, handler.initialize(kwargs))
        (r"/", MainHandler, kwargs),
        (r"/api/greet", MainHandler, kwargs),
        (r"/api/history", ChatHistoryHandler, kwargs),
        (r"/websocket", SocketHandler, kwargs),
    ]

