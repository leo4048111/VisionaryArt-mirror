# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common, db_tool

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        sql = "select uid, name, ip, regdate, stat from user where 1=1"
        results = db_tool.query(sql)
        for result in results:
            result['regdate'] = result['regdate'].isoformat()
            
        return self.finish(common.Ok(data=results))
