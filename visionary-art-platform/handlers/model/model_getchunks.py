# -*- coding: utf8 -*-
import os
import time

import tornado.web

from handlers import BaseHandler
from utils import common, time_tool, db_tool, path

# Use a global dict to save upload file info
FileChunkSet = {}

class Handle(BaseHandler):
    """ get user info """

    def initialize(self):
        self.chunk_size = 20 * 1024 * 1024  # 20MB/chunk
        self.must_have_params = []

    def post(self):
        # check if the file save dir is already existed
        type = common.my_str(self.get_argument('type', ''))
        file_save_dir = os.path.join(path.UPLOAD_FILES_ABSPATH, path.MODEL_UPLOAD_SAVE_PATH_PREFIX, type)

        if not os.path.exists(file_save_dir):
            os.makedirs(file_save_dir)

        uid = common.my_int(self.get_argument('uid'))
        filename = self.get_argument('filename', '')
        filesize = int(self.get_argument('filesize', 0))
        # get file extension with filename
        file_extention = os.path.splitext(filename)[1]
        fuid=str(hash(str(uid)+filename+str(filesize)))

        if FileChunkSet.__contains__(fuid) == True:
            return self.finish(common.Ok(data=FileChunkSet[fuid]))

        # Generate uid for this file
        saved_fname = filename
        data = self.calchunks(fuid=fuid, filesize=filesize, fname=saved_fname)

        # Save fuid for chunk file
        if FileChunkSet.__contains__(fuid) == False:
            FileChunkSet[fuid] = data

        # Create empty file with space allocated
        self.crate_empty_file(os.path.join(file_save_dir, saved_fname), filesize)

        return self.finish(common.Ok(data=data))

    def crate_empty_file(self, filename: str, filesize: int):
        with open(filename, 'wb') as fp:
            fp.seek(filesize-1)
            fp.write(b'\0')

    def calchunks(self, fuid: str, filesize: int, fname:str):
        # generate a unique id for file
        data = dict(
            fuid=fuid,
            fname=fname,
            chunks=[]
        )

        # calculate total chunks
        cnt = int(filesize/self.chunk_size)

        for i in range(0, cnt):
            chunk = {
                'chunk_size': self.chunk_size,
                'uploaded_size': 0
            }
            data['chunks'].append(chunk)
        last_chunk_size = filesize % self.chunk_size

        # append last chunk
        if last_chunk_size > 0:
            chunk = {
                'chunk_size': last_chunk_size,
                'uploaded_size': 0
            }
            data['chunks'].append(chunk)

        return data

if __name__ == "__main__":
    pass
