# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common, db_tool

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        sql = "select id, fuid, modelname, type, size, uid, upload_time from model where 1=1"
        results = db_tool.query(sql)
        for result in results:
            result['upload_time'] = result['upload_time'].isoformat()
            
        return self.finish(common.Ok(data=results))
