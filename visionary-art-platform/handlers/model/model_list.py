# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from utils import db_tool


class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.must_have_params = []

    def post(self):
        model_type = common.my_str(self.get_argument('model_type', 'Checkpoint'))
        uid = common.my_int(self.get_argument('uid', 0))
        list_type = common.my_str(self.get_argument('list_type', 'All'))
        result = []
        if list_type == 'All':
            args=dict(
                type=model_type,
            )
            sql = "select path from model where type=:type"
            result = db_tool.query(sql, **args)
        elif list_type == 'Liked':
            args=dict(
                uid=uid,
                type=model_type,
            )
            sql = "select path from model where id in (select mid from user_like_model where uid=:uid) and type=:type"
            result = db_tool.query(sql, **args)
        elif list_type == 'Uploaded':
            args=dict(
                uid=uid,
                type=model_type,
            )
            sql = "select path from model where uid=:uid and type=:type"
            result = db_tool.query(sql, **args)

        return self.finish(common.Ok(data=result))

if __name__ == "__main__":
    pass
