# -*- coding: utf8 -*-
from configs import err_conf
from utils import common, db_tool
import sys
import os

base_path = os.path.join(os.path.dirname(__file__) + '/../../')

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        # self.redis_handle = common.redis_handle()
        self.db_columns = [
            "id", "modelname", "path","uid","liked","upload_time","disc","version"
        ]
        self.columns = ",".join(self.db_columns)

    def remove_model(self, args):
        # query the model record and store the url of the model and then to delete native file
        sql = "select id, path from model where id = :id".format(
            columns = self.columns
        )
        
        result = db_tool.query(sql, **args)

        #这里要判一下空，以免查询结果为空直接访问[0]
        if len(result) == 0:
            return common.ok()
        
        model_path = result[0]["path"]

        # 先删除模型有关的评论
        sql = "delete from comment where mid = :id"
        result = db_tool.query(sql, **args)

        # 再删除模型有关的点赞
        sql = "delete from user_like_model where mid = :id"
        result = db_tool.query(sql, **args)
        
        # 后删除模型（避免因数据库表的完整性约束导致删除失败）
        sql = "delete from model where id = :id"
        result = db_tool.query(sql, **args)

        # delete model file
        if os.path.exists(model_path):
            os.remove(model_path)
        
        return common.Ok("Model has been deleted successfully")
    
    def if_user_like_model(self, args):
        sql = "select * from user_like_model where uid=:uid and mid=:mid"
        result = db_tool.query(sql, **args)
        data = dict(
            result=False
        )

        if len(result) != 0:  # 没有点赞过
            data['is_model_liked'] = True

        # get new liked cnt
        sql = "select liked from model where id=:mid"
        result = db_tool.query(sql, **args)
        data['liked'] = result[0]['liked']

        return common.Ok(data=data)