# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        import json
        data = json.loads(self.request.body)
        username = common.my_str(data["username"])
        password = common.my_str(data["password"])

        args = dict(
            name=username,
            password=password,
        )

        result = self.admin_handle.login_admin(args)
        
        return self.finish(result)
