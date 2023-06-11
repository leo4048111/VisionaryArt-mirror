# -*- coding: utf8 -*-
from configs import err_conf
from utils import common, auth_tool, db_tool
import sys

sys.path.append("..")
# from utils.log import send_try_except
# from utils import qiniu_tools

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        # self.redis_handle = common.redis_handle()
        self.db_columns = [
            "uid", "name", "regdate", "stat", "password", "sid", "avatar"
        ]
        self.columns = ",".join(self.db_columns)

    def validate_user_session(self, args):
        """validate user session"""
        result = auth_tool.validate_user_session(**args)

        if not result:
            return common.Err(err_conf.E_BAD_SESSION)

        return common.Ok()

    def logout_user(self, args):
        """logout user"""
        if not auth_tool.validate_user_session(args['uid'], args['session_key']):
            return common.Err(err_conf.E_BAD_SID)
        auth_tool.remove_user_session_key(args['uid'])
        args.pop('session_key')
        self.update_user_info(args)
        return common.Ok("User logout successfully")

    def login_user(self, args):
        """login user"""
        sql = "select {columns} from user where user.name=:name".format(
            columns=self.columns)
        result = db_tool.query(sql, **args)
        if len(result) == 0:
            return common.Err(err_conf.E_USER_NOT_EXIST)
        user_info = result[0]
        if user_info['stat'] == 'banned':
            return common.Err(err_conf.E_USER_BANNED)
        # if auth_tool.find_user_session_key(user_info['uid']) is not None:
        #     return common.Err(err_conf.E_USER_ALREADY_LOGGED_IN)

        # user_info['sid'] = auth_tool.get_user_sid(user_info['uid'])
        password = common.hash_password(args['password'], user_info['sid'])

        if password != user_info["password"]:
            auth_tool.remove_user_session_key(user_info['uid'])
            return common.Err(err_conf.E_WRONG_PASSWORD)
        user_info["password"] = "******"
        user_info['regdate'] = user_info['regdate'].isoformat()
        session_key, ttl = auth_tool.get_user_session_key(user_info['uid'])
        user_info['session_key'] = session_key
        user_info['ttl'] = ttl
        user_info.pop('sid')
        args = dict(
            uid=user_info['uid'],
            stat='online'
        )
        result = self.update_user_info(args)
        return common.Ok("User login successfully", data=user_info)

    def register_user(self, args):
        """register user"""

        sql = "select uid from user where name=:name"

        result = db_tool.query(sql, **args)
        if len(result) != 0:
            return common.Err(err_conf.E_USER_EXIST)

        sql = "insert into user(name, ip, regdate, stat, password, sid) values(:name, :ip, :regdate, :stat, :password, :sid)"
        db_tool.query(sql, **args)

        user_info = {}
        sql = "select uid from user where name=:name"
        result = db_tool.query(sql, **args)
        user_info['uid'] = result[0]['uid']

        user_info['sid'] = auth_tool.generate_user_sid(user_info['uid'])
        user_info['password'] = common.hash_password(args['password'], user_info['sid'])
        user_info['stat'] = 'offline'
        
        if 'avatar' in args:
            user_info['avatar'] = args['avatar']

        self.update_user_info(user_info)

        return common.Ok(msg="user registered successfully")

    def get_user_info(self, args):
        """get user info"""
        sql = "select {columns} from user where user.uid=:uid".format(
            columns=self.columns)
        result = db_tool.query(sql, **args)
        if len(result) == 0:
            return common.Err(err_conf.E_USER_NOT_EXIST)
        
        user_info = result[0]
        user_info['regdate'] = user_info['regdate'].isoformat()
        return common.Ok(data=user_info)

    def update_user_info(self, args):
        """update user info"""
        format_columns = []

        sql = "select {columns} from user where uid=:uid".format(
            columns=self.columns
        )

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
        return common.Ok("User info updated successfully")

if __name__ == '__main__':
    pass
