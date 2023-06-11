# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common

class Handle(BaseHandler):
    """
    modify user info
    """
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.user_handle = admin_handle.Handle()

    def post(self):
        uid = common.my_int(self.get_argument('uid'))
        name = common.my_str(self.get_argument('name', None))
        stat = common.my_str(self.get_argument('stat', None))
        password = common.my_str(self.get_argument('password', None))

        if name is not None:
            name=common.text_filter(name)

        args = dict(
            uid=uid,
            name=name,
            stat=stat,
            password=password
        )
        
        self.user_handle.update_user_info(args)

        return self.finish(common.Ok())
