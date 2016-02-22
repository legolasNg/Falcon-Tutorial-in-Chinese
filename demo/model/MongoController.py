# -*- coding: utf-8 -*-
import pymongo
import json
import os

import falcon


class StorageEngine(object):

    def __init__(self):
        #查找配置文件
        HOME_PATH = os.environ['HOME']
        self.config_file_path = ''.join([HOME_PATH, '/.cobweb_config.json'])
        print self.config_file_path
        if not os.path.isfile(self.config_file_path):
            print 'file can not be found '

        #从配置文件中读取数据库信息
        with file(self.config_file_path, 'r') as f:
            print 'database connected'
            self.config = json.loads(f.read())

        #连接数据库
        self.database = pymongo.MongoClient(self.config['HOST'], self.config['PORT'])[self.config['DB_NAME']]


class StorageError(Exception):

    @staticmethod
    def handle(ex, req, resp, params):
        description = u'错误，不能将数据写入数据库'

        raise falcon.HTTPError(falcon.HTTP_725,
                               'Database Error',
                               description)