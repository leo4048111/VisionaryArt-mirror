# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.image import image_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['count']
        self.image_handle = image_handle.Handle()

    def post(self):
        count = common.my_int(self.get_argument("count"))
        count = min(count, 20)
        uid = common.my_int(self.get_argument("uid", 0))

        args = dict(
            count=count,
            uid=uid
        )

        result = self.image_handle.image_get(args)
        
        return self.finish(result)
