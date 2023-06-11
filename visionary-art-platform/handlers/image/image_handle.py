# -*- coding: utf8 -*-
from configs import err_conf
from utils import common, db_tool
import sys
import os

base_path = os.path.join(os.path.dirname(__file__) + '/../../')

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()

    def image_share(self, args):
        sql = "select id from image where :path = path"
        result = db_tool.query(sql, **args)
        if len(result) != 0:
            return common.Err(e_msg="Image already shared, please dont reshare.")

        sql = "insert into image (path, generation_info_html, uid) values (:path, :generation_info_html, :uid)"
        db_tool.query(sql, **args)
        return common.Ok(msg="Done. Your image has been shared on Visionary Art. Check out via gallery in navigation bar.")
    
    def image_get(self, args):
        # sql = "select * from image where id >= (select floor(RAND() * (select max(id) from image))) order by id limit :count"
        sql = "select * from image order by rand() limit :count"
        # TODO: get images by uid

        results = db_tool.query(sql, **args)

        import urllib.request
        
        for res in results:
            res['generation_info_html'] = urllib.request.unquote(res['generation_info_html'])

        return common.Ok(data=results)