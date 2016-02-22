# -*- coding: utf-8 -*-
import falcon
from wsgiref import simple_server

from resource.Order import User, Company, Department, Group, Relation
from model.MongoController import StorageEngine
from middleware.JSONTranslator import JSONTranslator


api = application = falcon.API(middleware=JSONTranslator())

# 将一系列resource实例化
db = StorageEngine()

user = User(db)
company = Company(db)
department = Department(db)
group = Group(db)
relation = Relation(db)


# 添加路由规则
api.add_route('/user/', user)


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()