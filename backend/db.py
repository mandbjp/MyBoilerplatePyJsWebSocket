#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from datetime import datetime
import time
import pymongo


class Db(object):
    def __init__(self):
        self.client = None
        self.db = None
        pass

    def connect(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.niconico

    def get_chats(self):
        collection = self.db.chats
        ret = []
        for index, doc in enumerate(collection.find().sort([['order', pymongo.ASCENDING]])):
            ret.append(_document_to_dict(doc))
            if index >= 100:
                break
        return ret

    def add_chat(self, name, message):
        collection = self.db.chats

        dt = datetime.now()
        timestamp = time.mktime(dt.timetuple())

        document = {
            "name": name,
            "message": message,
            "timestamp": timestamp,
        }
        ret = collection.insert_one(document)
        if not ret.acknowledged:
            raise Exception("add_chat error")

        return _document_to_dict(document)


def _document_to_dict(document):
    d = document.copy()
    d["id"] = str(d["_id"])
    del d["_id"]
    return d
