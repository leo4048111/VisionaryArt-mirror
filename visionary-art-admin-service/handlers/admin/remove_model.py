# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.admin import admin_handle
from utils import common

class Handle(BaseHandler):
    """
    admin remove model
    """
    def initialize(self):
        self.must_have_params = []
        self.admin_handle = admin_handle.Handle()

    def post(self):
        import json
        data = json.loads(self.request.body)
        id = common.my_int(data["id"])
        args = dict(
            id = id,
        )
        
        self.admin_handle.remove_model(args)
        
        return self.finish(common.Ok("remove seccussfully"))
