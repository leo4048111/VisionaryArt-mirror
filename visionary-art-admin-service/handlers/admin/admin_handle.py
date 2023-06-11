# -*- coding: utf8 -*-
from configs import err_conf
from utils import common, auth_tool, db_tool
import sys
import os

sys.path.append("..")
# from utils.log import send_try_except
# from utils import qiniu_tools

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        self.db_columns = [
            "id", "modelname", "path","uid","liked","upload_time","disc","version","cover_pic"
        ]
        self.columns = ",".join(self.db_columns)

    def validate_user_session(self, args):
        """validate user session"""
        result = auth_tool.validate_user_session(**args)

        if not result:
            return common.Err(err_conf.E_BAD_SESSION)

        return common.Ok()

    def logout_admin(self, args):
        """logout user"""
        auth_tool.remove_user_session_key(args['uid'])
        self.update_admin_info(args)
        return common.Ok("Admin logout successfully")

    def login_admin(self, args):
        """login admin"""
        sql = "select uid, password, stat from admin where admin.name=:name"
        result = db_tool.query(sql, **args)
        if len(result) == 0:
            return common.Err(err_conf.E_USER_NOT_EXIST)
        admin_info = result[0]
        if admin_info['stat'] == 'banned':
            return common.Err(err_conf.E_USER_BANNED)

        password = common.hash_password(args['password'])

        if password != admin_info["password"]:
            auth_tool.remove_user_session_key(admin_info['uid'])
            return common.Err(err_conf.E_WRONG_PASSWORD)
        admin_info["password"] = "******"
        session_key, ttl = auth_tool.get_user_session_key(admin_info['uid'])
        admin_info['token'] = session_key
        admin_info['ttl'] = ttl
        args = dict(
            uid=admin_info['uid'],
            stat='online'
        )
        result = self.update_admin_info(args)
        return common.Ok("Admin login successfully", data=admin_info)

    def register_admin(self, args):
        """register admin"""

        args['password'] = common.hash_password(args['password'])
        sql = "select uid from admin where name=:name"

        result = db_tool.query(sql, **args)
        if len(result) != 0:
            return common.Err(err_conf.E_USER_EXIST)

        sql = "insert into admin(name, stat, password) values(:name, :stat, :password)"
        db_tool.query(sql, **args)

        return common.Ok(msg="admin registered successfully")

    def get_admin_info(self, args):
        """get user info"""
        sql = "select name from admin where admin.uid=:uid"
        result = db_tool.query(sql, **args)
        if len(result) == 0:
            return common.Err(err_conf.E_USER_NOT_EXIST)
        
        admin_info = result[0]
        admin_info['avatar'] = "https://c8.alamy.com/comp/JAM84D/beautiful-young-happy-muslim-woman-in-hijab-vector-flat-icon-avatar-JAM84D.jpg"
        return common.Ok(data=admin_info)

    def update_admin_info(self, args):
        """update admin info"""
        format_columns = []

        sql = "select uid from admin where uid=:uid"

        result = db_tool.query(sql, **args)

        if len(result) == 0:
            return common.Err(err_conf.E_USER_NOT_EXIST)

        for k, v in args.items():
            if v is None:
                continue
            if k == 'uid':
                continue
            format_columns.append("{0}=:{1}".format(k, k))
        format_columns = ','.join(format_columns)

        sql = "update user set {columns} where uid=:uid".format(
            columns=format_columns)
        
        db_tool.query(sql, **args)
        return common.Ok("Admin info updated successfully")
    
    def remove_model(self, args):
        # query the model record and store the url of the model and then to delete native file
        sql = "select id, path,cover_pic from model where id = :id".format(
            columns = self.columns
        )
        
        result = db_tool.query(sql, **args)

        #这里要判一下空，以免查询结果为空直接访问[0]
        if len(result) == 0:
            return common.ok()
        
        model_path = result[0]["path"]
        prefix =  model_path[:model_path.find("uploads")] 
        postfix = result[0]["cover_pic"][1:]
        model_cov = prefix + postfix

        # 先删除模型有关的评论
        sql = "delete from comment where mid = :id"
        result = db_tool.query(sql, **args)

        # 再删除模型有关的点赞
        sql = "delete from user_like_model where mid = :id"
        result = db_tool.query(sql, **args)
        
        # 后删除模型以及模型图片（避免因数据库表的完整性约束导致删除失败）
        sql = "delete from model where id = :id"
        result = db_tool.query(sql, **args)

        # 删除模型封面图片
        if os.path.exists(model_cov):
            os.remove(model_cov)
            
        # 删除模型文件
        if os.path.exists(model_path):
            os.remove(model_path)
        
        return common.Ok("Model has been deleted successfully")

if __name__ == '__main__':
    pass
