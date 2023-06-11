import os

from configs import err_conf
from utils import common, auth_tool, db_tool
from utils.path import MODEL_UPLOAD_SAVE_PATH_PREFIX

class Handle():
    def __init__(self):
        self.db_handle = common.db_handle()

    def search_user(self, args):
        """validate user session"""

        # there is a weirDass syntax belike ":search_name '%'", idk why it works only when a space is in between
        sql = "select uid, name, avatar, stat from user where name like :search_name '%'"
        result = db_tool.query(sql, **args)

        return common.Ok(data=result)

    def search_model(self, args):
        """validate user session"""

        if(args['liked'] != 0):
            sql = "select id, modelname, type, size, url, cover_pic, upload_time, disc, liked, version, avatar from model join user on model.uid = user.uid where model.id in (select mid from user_like_model where uid = :uid)"
            result = db_tool.query(sql, **args)
            for i in range(len(result)):
                result[i]['upload_time'] = result[i]['upload_time'].isoformat()
            return common.Ok(data=result)

        if(args['trending'] != 0):
            sql = "select id, modelname, type, size, url, cover_pic, upload_time, disc, liked, version, avatar from model join user on model.uid = user.uid order by model.liked limit :trending"
            result = db_tool.query(sql, **args)
            for i in range(len(result)):
                result[i]['upload_time'] = result[i]['upload_time'].isoformat()
            return common.Ok(data=result)

        sql = "select id, modelname, type, size, url, cover_pic, upload_time, disc, liked, version, avatar from model join user on model.uid = user.uid where {0}"
        sql_fname = "modelname like {}"
        pattern = ''
        if args['modelname'] != '':
            pattern = "'%' :modelname '%'"
        if args['filetype'] != '':
            if pattern == '':
                pattern += "'%'"
            pattern += " :filetype"

        if pattern != '':
            pattern = sql_fname.format(pattern)

        if args['uploader_uid'] != '':
            if pattern != '':
                pattern += " and "
            pattern += "user.uid = :uploader_uid"

        sql = sql.format(pattern)
        result = db_tool.query(sql, **args)
        for i in range(len(result)):
            result[i]['upload_time'] = result[i]['upload_time'].isoformat()
        return common.Ok(data=result)
