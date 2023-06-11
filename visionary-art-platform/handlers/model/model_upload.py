# -*- coding: utf8 -*-
import os
import time

from handlers import BaseHandler
from utils import common, time_tool, db_tool, path

class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.must_have_params = ['modelname']

    def post(self):
        # get files uploaded and save it

        # check if the file save dir is already existed
        type = common.my_str(self.get_argument('type', ''))
        file_save_dir = os.path.join(path.UPLOAD_FILES_ABSPATH, path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type)

        if not os.path.exists(file_save_dir):
            os.mkdir(file_save_dir)

        files = self.request.files

        # save model file
        model_file = files.get("modelfile", None)[0]
        model_file_data = model_file.get('body')
        model_file_name = model_file.get('filename')
        fname_model = os.path.join(file_save_dir, model_file_name)

        with open(fname_model, 'wb') as fp:
            fp.write(model_file_data)

        # save cover image file
        cover_image_file = files.get("coverimage", None)[0]
        if cover_image_file is not None:
            cover_image_data = cover_image_file.get('body')
            cover_image_name = cover_image_file.get('filename')
            with open(os.path.join(file_save_dir, cover_image_name), 'wb') as fp:
                fp.write(cover_image_data)
                fp.close()
        else:
            cover_image_name = 'default_cover_img.jpeg'

        size = common.my_int(self.get_argument('size', 0))
        uid = common.my_int(self.get_argument('uid'))
        fuid=str(hash(str(uid)+model_file_name+str(size)))
        modelname = common.my_str(self.get_argument('modelname', ''))
        model_path = common.my_str(fname_model)
        cover_pic = common.my_str(os.path.join('/', path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type, cover_image_name))
        url = common.my_str(os.path.join('/', path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type, model_file_name))
        liked = common.my_int(0)
        upload_time = time_tool.date_format(time.time())
        disc = common.my_str(self.get_argument('disc', ''))
        version = common.my_str(
            self.get_argument('version', 'unknown version'))

        args = dict(
            fuid=fuid,
            modelname=modelname,
            type=type,
            size=size,
            path=model_path,
            cover_pic=cover_pic,
            url=url,
            uid=uid,
            liked=liked,
            upload_time=upload_time,
            disc=disc,
            version=version
        )
        
        sql = "insert into model (fuid, modelname, type, size, path, url, cover_pic, uid, liked, upload_time, disc, version) values(:fuid, :modelname, :type, :size, :path, :url, :cover_pic, :uid, :liked, :upload_time, :disc, :version)"
        db_tool.query(sql, **args)

        return self.finish(common.Ok(msg="Model uploaded succesfully"))


if __name__ == "__main__":
    pass
