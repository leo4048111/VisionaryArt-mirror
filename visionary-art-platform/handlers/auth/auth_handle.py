'''
Author: leo4048111
Date: 2023-03-01 13:44:51
LastEditTime: 2023-03-04 14:46:35
LastEditors: ***
Description: 
FilePath: \tornado-bilibili-data-fetcher-analysis-persistence\handlers\auth\auth_handle.py
'''
# -*- coding: utf8 -*-

import sys

sys.path.append("../..")
import hashlib
from utils import common
import random, string

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()
        self.db_redis = common.redis_handle()
        # self.queue_handle = queue_tools.Handle()

    # def bind_phone(self, uid, phone):
    #     """绑定手机号操作"""
    #     sql = """
    #     update user_info set phone=:phone where uid=:uid
    #     """
    #     self.db_handle.query(sql, phone=phone, uid=uid)

    # def get_uid_by_phone(self, phone):
    #     """根据手机号获取uid"""
    #     sql = "select uid from user_info where phone=:phone and status=0"
    #     result = self.db_handle.query(sql, phone=phone)
    #     return result[0].uid if result.first() else 0

    # def save_wechat_openid_info(self, args):
    #     """保存微信授权登录的信息"""
    #     sql = """
    #     insert into openid_info set open_id=:open_id, source=:source, uid=:uid,
    #     status=:status, nick=:nick, sex=:sex, head_url=:head_url, union_id=:union_id,
    #     type=:type on duplicate key update
    #     source=:source, uid=:uid, status=:status, nick=:nick, sex=:sex,
    #     head_url=:head_url, union_id=:union_id
    #     """
    #     self.db_handle.query(sql, **args)

    # def get_uid_by_openid(self, openid):
    #     """通过open_id 获取 uid"""
    #     sql = """
    #     select uid from openid_info where open_id=:open_id
    #     """
    #     result = self.db_handle.query(sql, open_id=openid)
    #     return result[0].uid if result.first() else 0

    # def get_phone_by_uid(self, uid):
    #     """通过uid 获取手机号"""
    #     sql = """
    #     select phone from user_info where uid=:uid and status=0
    #     """
    #     result = self.db_handle.query(sql, uid=uid)
    #     return result[0].phone if result.first() else ''

    # def deal_with_head_url(self, uid, head_url):
    #     '''
    #     后续处理
    #     '''
    #     task_name = "wwd_upload_head_url"
    #     job_data = {"head_url": head_url}
    #     self.queue_handle.add_to_queue(uid, task_name, job_data)

if __name__ == '__main__':
    handle = Handle()
    print(handle.genarate_session_key())
