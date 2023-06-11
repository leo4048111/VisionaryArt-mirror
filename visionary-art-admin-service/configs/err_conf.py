'''
Author: leo4048111
Date: 2023-03-01 13:44:51
LastEditTime: 2023-03-04 21:28:36
LastEditors: ***
Description: error definitions
'''
# -*- coding: utf-8 -*-
ES_BAD_PARAM = 'Invalid parameter'
E_EXCEPTION = -102
ES_EXCEPTION = 'Internal error'
E_BAD_SID = (4004, "User SID invalid or expired")
E_BAD_SESSION = (7007, "User session expired, please relogin")
E_BAD_PHONE = (1000, "Invalid phone number, please re enter")
E_BAD_CHECK_PHONE_CODE = (1001, "验证码输入有误，请重新输入。")
E_PHONE_CODE_EXPIRE = (1002, "验证码已过期，请重新发送。")
E_BAD_WX_AUTH = (1003, "微信授权登录失败！")
E_BAD_UPLOAD_HEAD = (1004, "上传失败")
E_BAD_BUSINESS_SOURCE = (1005, "错误的业务类型")
E_USER_EXIST = (1006, "User already exists")
E_USER_NOT_EXIST = (1007, "User doesn't exist")
E_WRONG_PASSWORD = (1008, "Wrong password")
E_USER_ALREADY_LOGGED_IN = (1009, "User already logged in")
E_ADMIN_NOT_EXIST = (1010, "管理员不存在")
E_ADMIN_ALREADY_EXIST = (1011, "管理员已存在")
E_ADMIN_ALREADY_LOGGED_IN = (1012, "管理员已登录")
E_ADMIN_ALREADY_LOGGED_OUT = (1013, "管理员已登出")
E_USER_BANNED = (1014, "User already banned")
E_BILIBILI_USER_BINDED = (1015, "Bilibili user has already been binded to another account")
E_BILIBILI_USER_NOT_EXIST = (1016, "Bilibili user doesn't exist")
E_USER_NOT_BIND = (1017, "User not bind, please bind your account to a bilibili account first")
