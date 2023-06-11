# coding:utf8

from handlers import BaseHandler
from handlers.user import user_handle
from utils import common, time_tool
import time

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['name', 'password']
        self.user_handle = user_handle.Handle()

    def post(self):
        name = common.my_str(self.get_argument("name"))
        password = common.my_str(self.get_argument("password"))
        regdate = time_tool.date_format(time.time())
        stat = common.my_str("banned")
        ip = self.request.headers.get('X-Real-Ip', '')
        if ip == "":
            ip = self.request.remote_ip
        ip = common.my_str(ip)
        sid = common.my_int(0)

        # just for tests
        avatar = common.my_str("/static/img/avatar.png")

        args = dict(
            name=name,
            ip=ip,
            password=password,
            regdate=regdate,
            stat=stat,
            sid=sid,
            avatar=avatar
        )

        response = self.user_handle.register_user(args)
        return self.finish(response)