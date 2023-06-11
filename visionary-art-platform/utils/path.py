import os
from utils.common import project_dir

UPLOAD_FILES_SAVE_PATH_PREFIX = 'uploads'
UPLOAD_FILES_ABSPATH = os.path.dirname(project_dir())
AVATAR_SAVE_PATH_PREFIX = os.path.join(UPLOAD_FILES_SAVE_PATH_PREFIX, 'avatar')
MODEL_UPLOAD_SAVE_PATH_PREFIX= os.path.join(UPLOAD_FILES_SAVE_PATH_PREFIX, 'models')
