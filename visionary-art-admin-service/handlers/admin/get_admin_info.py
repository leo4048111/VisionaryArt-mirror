# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from handlers.admin import admin_handle

class Handle(BaseHandler):
    """ get admin info """
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def get(self):
        uid = common.my_int(self.get_argument('token'))
        args = dict(
            uid=uid
        )
        result = self.admin_handle.get_admin_info(args)
        return self.finish(result)

if __name__ == "__main__":
    pass
