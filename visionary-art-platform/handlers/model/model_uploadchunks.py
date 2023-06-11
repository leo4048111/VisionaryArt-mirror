# -*- coding: utf8 -*-
import os
import time

import tornado.web

from handlers import BaseHandler
from utils import common, time_tool, db_tool, path

from handlers.model.model_getchunks import FileChunkSet

class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.must_have_params = []

    def post(self):
        files = self.request.files
        chunk_index = common.my_int(self.get_argument('chunk_index'))
        fuid = self.get_argument('fuid','')

        # check if the file save dir is already existed
        type = common.my_str(self.get_argument('type', ''))
        file_save_dir = os.path.join(path.UPLOAD_FILES_ABSPATH, path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type)
        fdata = FileChunkSet[fuid]
        fname_model = os.path.join(file_save_dir, fdata['fname'])

        if chunk_index == -1:
            cover_image_file = files.get("coverimage", None)[0]
            if cover_image_file is not None:
                cover_image_data = cover_image_file.get('body')
                cover_image_name = cover_image_file.get('filename')
                with open(os.path.join(file_save_dir, cover_image_name), 'wb') as fp:
                    fp.write(cover_image_data)
            else:
                cover_image_name = 'default_cover_img.jpeg'
            modelname = common.my_str(self.get_argument('modelname', ''))
            size = common.my_int(self.get_argument('size', 0))
            model_path = common.my_str(fname_model)
            cover_pic = common.my_str(os.path.join('/', path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type, cover_image_name))
            url = common.my_str(os.path.join('/', path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type, fdata['fname']))
            uid = common.my_int(self.get_argument('uid'))
            liked = common.my_int(0)
            upload_time = time_tool.date_format(time.time())
            disc = common.my_str(self.get_argument('disc', ''))
            version = common.my_str(
                self.get_argument('version', 'unknown version'))

            args = dict(
                modelname=modelname,
                fuid=fuid,
                type=type,
                size=size,
                path=model_path,
                url=url,
                cover_pic=cover_pic,
                uid=uid,
                liked=liked,
                upload_time=upload_time,
                disc=disc,
                version=version
            )

            sql = "insert into model (fuid, modelname, type, size, path, url, cover_pic, uid, liked, upload_time, disc, version) values(:fuid, :modelname, :type, :size, :path, :url, :cover_pic, :uid, :liked, :upload_time, :disc, :version)"
            db_tool.query(sql, **args)
            
            # if query succeeds, remove the file chunk set
            FileChunkSet.pop(fuid)
            return self.finish(common.Ok(msg="Model uploaded succesfully"))

        if not os.path.exists(file_save_dir):
            os.makedirs(file_save_dir)

        chunks = FileChunkSet[fuid]['chunks']
        pos = int(self.get_argument('pos'))
        if FileChunkSet.__contains__(fuid) == False:
            return self.finish(common.Err(e_msg='No chunk file id found'))
        
        # save model file segment
        model_file = files.get("file", None)[0]
        model_file_data = model_file.get('body')
        with open(fname_model, 'rb+') as fp:
            fp.seek(pos)
            fp.write(model_file_data)
            fp.close()

        chunks[chunk_index]['uploaded_size'] = chunks[chunk_index]['chunk_size']

        return self.finish(common.Ok(msg="chunk {} ok".format(chunk_index)))
    
    def isFileIntegrated(self, fuid: str):
        fdata = FileChunkSet[fuid]
        for chunk in fdata['chunks']:
            if chunk['chunk_size'] != chunk['uploaded_size']:
                return False
        return True

if __name__ == "__main__":
    pass
