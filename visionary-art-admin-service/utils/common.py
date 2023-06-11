#!/usr/bin/pyton
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("..")
from utils import db_redis, db_mysql
import hashlib

def project_dir():
    path = os.path.dirname(os.path.dirname(__file__))
    return path

def root_dir():
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return path

def my_int(input_data):
    """
    my_int操作
    """
    output_data = 0
    try:
        output_data = int(float(input_data))
    except ValueError:
        pass
    return output_data


def my_long(input_data):
    """
    my_long操作
    """
    output_data = 0
    try:
        output_data = long(float(input_data))
    except ValueError:
        pass
    return output_data


def my_float(input_data):
    """
    my_float操作
    """
    output_data = 0.0
    try:
        output_data = float(input_data)
    except ValueError:
        pass
    return output_data


def Err(e_msg='', e_code=2, data=None):
    """
    返回Err
    """
    if isinstance(e_msg, tuple):  # 兼容tuple传参
        e_code, e_msg = e_msg[0], e_msg[1]
    return {'code': int(e_code), 'msg': e_msg, 'flag': 0, 'data': data}


def BadParam(key, code=2):
    """
    返回参数错误
    """
    msg = "Param [%s] Error or Missing?" % (key)
    return {'code': int(code), 'msg': msg, 'flag': 0}


def my_str(input):
    """
    my_str操作
    """
    try:
        from tornado import escape
        output = escape.native_str(input)
        if output and len(output) > 30 and '<' in output and '>' in output:
            import pxfilter
            parser = pxfilter.XssHtml()
            parser.feed(output)
            parser.close()
            output = parser.getHtml()
    except Exception:
        output = str(input)
    return output

def Ok(msg="ok", data=None):
    """
    return ok
    """
    return {"code": 0, "msg": msg, "cnt": 1, "flag": 0, "data": data}

def redis_handle():
    """redis tools"""
    return db_redis.DBRedis.GetRedis()

def db_handle():
    """db mysql"""
    return db_mysql.DBMySql.GetMySql("db")

def is_right_phone(s):
    # 号码前缀，如果运营商启用新的号段，只需要在此列表将新的号段加上即可。
    phoneprefix = [
        '173', '154', '179', '175', '145', '149', '176', '170', '147', '184',
        '178', '177', '181', '153', '180', '157', '185', '155', '156', '189',
        '188', '183', '182', '133', '187', '132', '152', '151', '130', '131',
        '134', '150', '159', '158', '186', '137', '136', '135', '139', '138',
        '147', '171', '166', '147', '199', '198', '191'
    ]
    if s.isdigit() and len(s) == 11 and s[:3] in phoneprefix:
        return True
    return False

def hash_password(password):
    s =  password
    password = hashlib.md5(s.encode("utf-8")).hexdigest()
    return password

# def get_user_head_url(user_id, size=80, protocal="https"):
#     """获取用户头像"""
#     from handlers.user import user_handle
#     if protocal != "https":
#         protocal = "http"
#     seq = user_id % 10 + 10000
#     head_val = user_handle.Handle().get_head_val(user_id)
#     head_name = "head_url/{seq}/wwd_head_{user_id}_{size}_{head_val}.jpg".format(
#         user_id=user_id, size=size, head_val=head_val, seq=seq)
#     head_url = "{protocal}://head-img.51yund.com/{head_name}".format(
#         protocal=protocal, head_name=head_name)
#     head_url = head_url + "?imageslim"
#     return head_url

# def table_handle_by_user_id(table, user_id):
#     '''
#     获取分表
#     '''
#     mod = user_id % 10
#     if table in ['user_hardware_data']:
#         mod = user_id % 10
#     table = table + "_{0}".format(mod)
#     return table

# def db_handle_by_table(table):
#     '''
#     获取db
#     '''
#     if table in ['user_hardware_data']:
#         return db_handle()

def text_filter(s):
    """
    sql特殊字段过滤
    """
    dirty_stuff = [
        "\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$",
        "(", ")", "%", "@", "!"
    ]
    for stuff in dirty_stuff:
        s = s.replace(stuff, "")
    return s


if __name__ == "__main__":
    pass