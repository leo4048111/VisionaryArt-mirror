# -*- coding: utf8 -*-
from handlers import BaseHandler
from utils import common
from handlers.search import search_handle

class Handle(BaseHandler):
    """ get user info """
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.search_handle = search_handle.Handle()

    def post(self):
        uid = common.my_int(self.get_argument('uid', 0))
        liked = common.my_int(self.get_argument('liked', 0))
        trending = common.my_int(self.get_argument('trending', 0))
        modelname = common.my_str(self.get_argument('modelname', ''))
        uploader_uid = common.my_str(self.get_argument('uploader_uid', ''))
        filetype = common.my_str(self.get_argument('filetype', ''))
        args = dict(
            uid=uid,
            liked=liked,
            trending=trending,
            modelname=modelname,
            uploader_uid=uploader_uid,
            filetype=filetype
        )
        result = self.search_handle.search_model(args)
        return self.finish(result)

if __name__ == "__main__":
    pass
