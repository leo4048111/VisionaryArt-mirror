# -*- coding: utf8 -*-
from handlers import BaseHandler
from handlers.user import user_handle
from utils import common,  db_tool

class Handle(BaseHandler):
    """ get user info """
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        #self.user_handle = user_handle.Handle()

    def post(self):
        mid = common.my_int(self.get_argument('mid'))
        #content=common.my_int(self.get_argument('content'))
        args = dict(
            mid=mid
        )
        sql = "select content,post_time,ip,avatar,name from (comment natural join user) where mid=:mid"
        
        result = db_tool.query(sql, **args)
        for i in range(len(result)):
            result[i]['post_time'] = result[i]['post_time'].isoformat()

        return self.finish(common.Ok(data=result))
