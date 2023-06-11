from handlers import BaseHandler
from utils import common
from handlers.user import user_handle

class Handle(BaseHandler):
    def initialize(self):
        self.must_have_params = ['uid', 'session_key']
        self.user_handle = user_handle.Handle()

    def post(self):
        uid = common.my_int(self.get_argument('uid', 0))
        session_key = common.my_str(self.get_argument('session_key', ''))

        args = dict(
            uid=uid,
            session_key=session_key
        )

        result = self.user_handle.validate_user_session(args)

        self.finish(result)