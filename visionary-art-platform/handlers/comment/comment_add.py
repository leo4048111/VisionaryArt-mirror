# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common, time_tool, db_tool
import time

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid', 'session_key', 'content', 'mid']

    def post(self):
        """validate user session"""
       
        post_time = time_tool.date_format(time.time())
        ip = self.request.headers.get('X-Real-Ip', '')
        if ip == "":
            ip = self.request.remote_ip
        ip = common.my_str(ip)
        content = common.my_str(self.get_argument('content'))
        uid = common.my_int(self.get_argument('uid'))
        mid = common.my_int(self.get_argument('mid',0))
        liked = common.my_int(0)

        args = dict(
            post_time=post_time,
            ip=ip,
            content=content,
            uid=uid,
            mid=mid,
            liked=liked
        )
        sql = "insert into comment (post_time, ip, content, uid, mid, liked) values(:post_time, :ip, :content, :uid, :mid, :liked)"
        db_tool.query(sql, **args)

        return self.finish(common.Ok(msg="Comment uploaded succesfully"))

#long live ycl
