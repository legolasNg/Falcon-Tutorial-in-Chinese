# -*- coding: utf-8 -*-
from hooks.ObjectId import string_to_objectid

import falcon


class Company(object):

    def __init__(self, db):
        self.db = db.database

    @falcon.before(string_to_objectid)
    def on_get(self, req, resp):
        result = self.db.company.find(req.params)
        #将pymongo生成的cursor格式转换成json格式

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        body = req.context['doc']
        result = self.db.company.insert(body)

        if req.context['result']:
            req.context['result'] = result
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_404


class Department(object):

    def __init__(self, db):
        self.db = db.database

    @falcon.before(string_to_objectid)
    def on_get(self, req, resp):
        result = self.db.department.find(req.params)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        body = req.context['doc']
        result = self.db.department.insert(body)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_404


class User(object):

    def __init__(self, db):
        self.db = db.database

    def on_post(self, req, resp):
        body = req.context['doc']
        if 'company' in body:
            company_ref = self.db.company.find_one({'name':body['company']})
            if company_ref:
                body['company'] = company_ref
        if 'department' in body:
            department_ref = self.db.department.fin_one({'name':body['department']})
            if department_ref:
                body['department'] = department_ref
        result = self.db.user.insert(body)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_404

    @falcon.before(string_to_objectid)
    def on_put(self, req, resp):
        body = req.context['doc']
        result = self.db.user.update(req.params, body)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_404

    @falcon.before(string_to_objectid)
    def on_get(self, req, resp):
        result = self.db.user.find(req.params)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    @falcon.before(string_to_objectid)
    def on_delete(self, req, resp):
        result = self.db.user.remove(req.params)

        if result:
            req.context['result'] = result
            resp.status = falcon.HTTP_202
        else:
            resp.status = falcon.HTTP_404


class Group(object):

    def __init__(self, db):
        self.db = db.database

    def on_get(self, req, resp, user_id):
        pass

    def on_post(self, req, resp, user_id):
        pass


class Relation(object):

    def __init__(self, db):
        self.db = db.database

    def on_get(self, req, resp, user_id):
        pass

    def on_post(self, req, resp, user_id):
        pass