# -*- coding: utf8 -*-
"""
获取session_key
"""

from handlers import BaseHandler
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['service_port', 'auth_key']
        self.redis_handle = common.redis_handle()

    def post(self):
        port = common.my_int(self.get_argument("service_port"))
        auth_key = common.my_str(self.get_argument("auth_key"))

        import hashlib
        if auth_key != hashlib.sha1('visionary-art-ai-service'.encode('utf-8')).hexdigest():
            return self.finish(common.Err('auth_key error'))
        
        self.redis_handle.set('ai_service_port', port, ex=7)

        return self.finish(common.Ok())
