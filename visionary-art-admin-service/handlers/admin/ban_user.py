# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from utils import common, db_tool, auth_tool

class Handle(BaseHandler):
    """ get admin info """
    def initialize(self):
        self.must_have_params = []

    def post(self):
        import json
        data = json.loads(self.request.body)
        uid = common.my_str(data["uid"])

        session_key = auth_tool.find_platform_user_session_key(uid)
        if session_key:
            auth_tool.remove_platform_user_session_key(uid)

        args=dict(
            uid=uid,
            stat='banned'
        )
        
        sql = "update user set stat=:stat where uid=:uid"
        db_tool.query(sql, **args)
        return self.finish(common.Ok("Suspend user successfully!"))

if __name__ == "__main__":
    pass