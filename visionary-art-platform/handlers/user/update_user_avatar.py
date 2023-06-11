# -*- coding: utf8 -*-
import os
import time

from handlers import BaseHandler
from utils import common, time_tool, db_tool, path

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid']

    def post(self):
        file_save_dir = os.path.join(path.UPLOAD_FILES_ABSPATH, path.AVATAR_SAVE_PATH_PREFIX)
        if not os.path.exists(file_save_dir):
            os.makedirs(file_save_dir)

        files = self.request.files

        # save avatar file
        uid = common.my_int(self.get_argument('uid'))
        avatar_file = files.get("avatarFile", None)[0]
        avatar_file_data = avatar_file.get('body')
        avatar_file_name = avatar_file.get('filename')
        avatar_file_name = 'avatar_{0}_{1}.jpg'.format(uid, int(time.time()))
        with open(os.path.join(file_save_dir, avatar_file_name), 'wb') as fp:
            fp.write(avatar_file_data)
        
        avatar = common.my_str(os.path.join('/', path.AVATAR_SAVE_PATH_PREFIX, avatar_file_name))

        args = dict(
            uid=uid,
            avatar=avatar
        )

        sql = "update user set avatar=:avatar where uid=:uid"
        db_tool.query(sql, **args)

        return self.finish(common.Ok(msg="Avatar updated succesfully"))


if __name__ == "__main__":
    pass
