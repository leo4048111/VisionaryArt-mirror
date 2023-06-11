# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from utils import db_tool


class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.must_have_params = ['uid', 'session_key', 'mid']
        # 跨数据库表获取，怎么做？
        #self.user_handle = user_handle.Handle()
        '''self.db_columns = [
            "uid", "mid"
        ]
        self.columns = ",".join(self.db_columns)'''

    def post(self):
        uid = common.my_int(self.get_argument('uid', 0))
        mid = common.my_int(self.get_argument('mid', 0))

        args = dict(
            uid=uid,
            mid=mid
        )

        sql = "select * from user_like_model where uid=:uid and mid=:mid"
        result = db_tool.query(sql, **args)

        # remove like
        if len(result) != 0:
            sql = "delete from user_like_model where uid=:uid and mid=:mid"
            db_tool.query(sql, **args)
            # total liked cnt -1
            sql = "update model set liked=liked-1 where id=:mid"
            db_tool.query(sql, **args)
            return self.finish(common.Ok("Removed model like successfully"))

        sql = "insert into user_like_model(uid, mid) values(:uid, :mid)"
        db_tool.query(sql, **args)
        # total liked cnt +1
        sql = "update model set liked=liked+1 where id=:mid"
        db_tool.query(sql, **args)

        return self.finish(common.Ok("Liked model successfully"))

        '''
        sql = "select liked from user_like_model where uid=:uid and mid=:mid"
        result = db_tool.query(sql, **args)
        
        if len(result) != 0:#之前已经存在相应点赞or取消点赞记录，更新即可
            sql="update user_like_model set liked=:liked where uid=:uid and mid=:mid"
            db_tool.query(sql, **args)
            return self.finish(common.OK("点赞成功！"))
        
        sql = "insert into user_like_model(uid, mid, liked) values(:uid, :mid, :liked)".format(
            columns=self.columns,
        )
        db_tool.query(sql, **args)        
        
        return self.finish(common.Ok("点赞成功！"))'''


if __name__ == "__main__":
    pass
