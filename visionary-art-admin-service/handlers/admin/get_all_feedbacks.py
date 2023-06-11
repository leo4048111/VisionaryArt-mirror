# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common, db_tool

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        sql = "select * from feedback where 1=1"
        results = db_tool.query(sql)
        for result in results:
            result['post_time'] = result['post_time'].isoformat()
            
        return self.finish(common.Ok(data=results))
