# -*- coding: utf-8 -*-
"""
改写tornado web 父类的一些方法
"""
import json

import tornado.web

from configs import err_conf
from configs.not_need_session import not_need_session
from utils import common, auth_tool
# from utils.log import ApiGrayUserlog_tornado, ApiGraylog, send_try_except

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        """
        actions before request is actually handled by get/post method
        """
        ret = self.check_must_have_param()
        if ret:
            return self.finish(ret)

        path = self.request.path
        # check login status
        if path not in not_need_session:
            if not self.request.headers.__contains__('X-Token'):
                return self.finish(common.Err(err_conf.E_BAD_SESSION))
            
            uid = common.my_int(self.request.headers['X-Token'])
            session_key = auth_tool.find_user_session_key(uid)
            if session_key is None:
                return self.finish(common.Err(err_conf.E_BAD_SESSION))

    def write(self, chunk):
        """
        把response存一下
        """
        self.response = chunk
        # 调用父类的write
        super(BaseHandler, self).write(chunk)

    def finish(self, chunk=None, code=None, msg=None):
        """
        请求结果finish
        """
        if chunk is None and code is None:
            chunk = dict(code=-102, msg="内部异常")
            # 上报异常
            # send_try_except(self.request)

        if isinstance(chunk, dict):
            if 'code' not in chunk:
                chunk.update(code=0)
            if 'msg' not in chunk:
                chunk.update(msg='ok')
            if code:
                chunk.update(code=code)
            if msg:
                chunk.update(msg=msg)
        self.response = chunk
        # # 日志上报
        # self.send_to_gray_log()
        super(BaseHandler, self).finish(chunk)

    def send_to_gray_log(self):
        """
        gray_log 日志上报
        """
        user_id = int(self.get_argument('user_id', 0))
        # ApiGrayUserlog_tornado(user_id, self.response, self.request, True)

    def parse_request_body(self):
        """prepare for get body arguments"""
        try:
            request_arguments = self.request.arguments
            if request_arguments:
                new_request_arguments = {
                    k: common.my_str(v[0].decode('utf8'))
                    for k, v in request_arguments.items()
                }
                return new_request_arguments
            else:
                request_body = self.request.body
                request_data = request_body.decode('utf-8')
                if request_data == '':
                    return {}
                request_data_dict = json.loads(request_data)
                self.request.arguments = {
                    k: [str(v)]
                    for k, v in request_data_dict.items()
                }
                new_request_arguments = {
                    k: common.my_str(v)
                    for k, v in request_data_dict.items()
                }
                return new_request_arguments
        except Exception as e:
            raise tornado.web.HTTPError(
                status_code=400, log_message='bad_request: {}'.format(str(e)))

    def check_must_have_param(self):
        args = self.request.arguments
        if not hasattr(self, "must_have_params"):
            return None
        for key in self.must_have_params:
            if key not in args.keys():
                return common.BadParam(key)
            if args[key] == None:
                return common.BadParam(key)
        return None

if __name__ == '__main__':
    pass
