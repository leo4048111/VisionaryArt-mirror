# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from utils import common, db_tool

class Handle(BaseHandler):
    """ get admin info """
    def initialize(self):
        self.must_have_params = []

    def post(self):
        import json
        data = json.loads(self.request.body)
        uid = common.my_str(data["uid"])
        args=dict(
            uid=uid,
            stat='offline'
        )
        
        sql = "update user set stat=:stat where uid=:uid"
        db_tool.query(sql, **args)
        return self.finish(common.Ok("Enable user successfully!"))

if __name__ == "__main__":
    pass