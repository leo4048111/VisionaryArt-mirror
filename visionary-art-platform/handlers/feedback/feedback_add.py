# -*- coding: utf8 -*-

from handlers import BaseHandler
from utils import common, time_tool, db_tool

import time

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['title', 'tag']

    def post(self):
        import json
        body = json.loads(self.request.body.decode('utf-8'))

        uid = common.my_int(self.get_argument("uid"))
        title = common.my_str(self.get_argument("title", ""))
        tag = common.my_str(self.get_argument("tag", ""))
        contact = common.my_str(self.get_argument("contact", ""))
        detail = common.my_str(body['detail'])
        post_time = time_tool.date_format(time.time())
        args = dict(
            uid=uid,
            title=title,
            tag = tag,
            contact = contact,
            detail = detail,
            post_time = post_time
        )

        sql = "insert into feedback (uid, title, tag, contact, detail, post_time) values(:uid, :title, :tag, :contact, :detail, :post_time)"
        
        db_tool.query(sql, **args)

        return self.finish(common.Ok())
