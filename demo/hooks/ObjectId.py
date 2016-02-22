# -*- coding: utf-8 -*-
from bson import ObjectId

import falcon


def string_to_objectid(req, resp, params):
    if '_id' in req.params:
        #将传入的id对应的字符转换成mongoDB中对应的ObjectId对象
        req.params.__setitem__('_id', ObjectId(req.params['_id']))