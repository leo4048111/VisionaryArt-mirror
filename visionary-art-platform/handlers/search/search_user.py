# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from handlers.search import search_handle

class Handle(BaseHandler):
    """ get user info """
    def initialize(self):
        self.must_have_params = ['uid', 'session_key', 'search_name']
        self.search_handle = search_handle.Handle()

    def post(self):
        search_name = common.my_str(self.get_argument('search_name'))
        args = dict(
            search_name=search_name
        )
        result = self.search_handle.search_user(args)
        return self.finish(result)

if __name__ == "__main__":
    pass
