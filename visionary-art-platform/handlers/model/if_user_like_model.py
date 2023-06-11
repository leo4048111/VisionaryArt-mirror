# -*- coding: utf8 -*-
from handlers import BaseHandler
from handlers.model import model_handle
from utils import common
from utils import db_tool


class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.must_have_params = ['uid', 'session_key', 'mid']
        # 跨数据库表获取，怎么做？
        #self.user_handle = user_handle.Handle()
        self.model_handle = model_handle.Handle()

    def post(self):
        uid = common.my_int(self.get_argument('uid', 0))
        mid = common.my_int(self.get_argument('mid', 0))

        args = dict(
            uid=uid,
            mid=mid
        )

        result = self.model_handle.if_user_like_model(args)

        return self.finish(result)
