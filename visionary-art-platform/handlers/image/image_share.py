# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.image import image_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = []
        self.image_handle = image_handle.Handle()

    def post(self):
        path = common.my_str(self.get_argument("path"))
        generation_info_html = common.my_str(self.get_argument("generation_info_html"))
        uid = common.my_int(self.get_argument("uid"))
        
        args = dict(
            path=path,
            generation_info_html=generation_info_html,
            uid=uid
        )

        result = self.image_handle.image_share(args)

        return self.finish(result)
