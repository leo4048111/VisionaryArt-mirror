# -*- coding: utf8 -*-
"""
获取session_key
"""

from handlers import BaseHandler
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.redis_handle = common.redis_handle()

    def post(self):
        port = common.my_str(self.redis_handle.get('ai_service_port'))

        if not port:
            port = 0

        return self.finish(common.Ok(data={'port': port}))
