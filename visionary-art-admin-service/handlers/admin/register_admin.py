# coding:utf8

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common
import time

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        name = common.my_str(self.get_argument("username"))
        password = common.my_str(self.get_argument("password"))
        stat = common.my_str("offline")

        args = dict(
            name=name,
            password=password,
            stat=stat,
        )

        response = self.admin_handle.register_admin(args)
        return self.finish(response)