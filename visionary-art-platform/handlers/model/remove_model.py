# -*- coding: utf8 -*-

from handlers import BaseHandler
from handlers.model import model_handle
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['mid']
        self.model_handle = model_handle.Handle()
    
    ## model 表结构完善，需要更改代码
    def post(self):
        id = common.my_int(self.get_argument("mid",0))

        args = dict(
            id = id,
        )
        
        self.model_handle.remove_model(args)
        
        return self.finish(common.Ok("remove seccussfully"))
