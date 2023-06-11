# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.user import user_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['name', 'password']
        self.user_handle = user_handle.Handle()

    def post(self):
        name = common.my_str(self.get_argument("name"))
        password = common.my_str(self.get_argument("password"))

        args = dict(
            name=name,
            password=password,
        )

        result = self.user_handle.login_user(args)
        
        return self.finish(result)
