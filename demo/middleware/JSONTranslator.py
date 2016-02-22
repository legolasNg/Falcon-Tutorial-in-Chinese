# -*- coding: utf-8 -*-
import falcon
import json
from bson import json_util
import pymongo


class JSONTranslator(object):

    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(u'请求body为空',
                                        u'请输入一个合法的JSON文档')

        try:
            #将请求中的数据的格式转换成utf-8
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   u'错误的JSON格式',
                                   u'不能解码请求的body. 请求JSON格式错误或者编码不是UTF-8')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        # 判断是否已经转换成json格式
        if type(req.context['result']) is pymongo.cursor.Cursor:
            #将pymongo生成的cursor格式转换成json格式
            resp.body = json_util.dumps(req.context['result'])
        else:
            resp.body = json.dumps(req.context['result'])