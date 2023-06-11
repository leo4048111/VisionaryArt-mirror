# -*- coding: utf8 -*-
 
from handlers import BaseHandler
from utils import common
from utils import db_tool
 
class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid', 'session_key','id']
        
    def post(self):
        id = common.my_int(self.get_argument('id',0))
        uid = common.my_int(self.get_argument('uid',0))

        args = dict(
            id=id
        )

        sql_check="select uid from comment where id=:id"
        result=db_tool.query(sql_check,**args)
        if len(result) == 0:
            return self.finish(common.Ok("此评论不存在!"))
        
        comment_uid=result[0]['uid']
        if comment_uid!=uid:
            return self.finish(common.Ok("你不能删除不是你发的评论!"))

        sql_remove="delete from comment where id=:id"
        db_tool.query(sql_remove,**args)
        
        return self.finish(common.Ok("评论删除成功!"))