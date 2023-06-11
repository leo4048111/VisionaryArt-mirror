# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from handlers.user import user_handle

class Handle(BaseHandler):
    """ get user info """
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.user_handle = user_handle.Handle()

    def post(self):
        uid = common.my_int(self.get_argument('uid'))
        args = dict(
            uid=uid
        )
        result = self.user_handle.get_user_info(args)
        return self.finish(result)

if __name__ == "__main__":
    pass
