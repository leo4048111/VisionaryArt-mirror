# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.user import user_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.user_handle = user_handle.Handle()

    def post(self):
        """
        user logout
        """
        uid = common.my_int(self.get_argument('uid'))
        session_key = common.my_str(self.get_argument('session_key'))
        args = dict(
            uid=uid, 
            session_key=session_key, 
            stat='offline')
        
        result = self.user_handle.logout_user(args)

        return self.finish(result)
