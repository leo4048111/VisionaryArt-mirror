# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        """
        user logout
        """
        uid = common.my_int(self.request.headers['X-Token'])
        args = dict(
            uid=uid, 
            stat='offline'
        )
        
        result = self.admin_handle.logout_admin(args)

        return self.finish(result)
