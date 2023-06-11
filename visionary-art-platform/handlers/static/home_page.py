from handlers import BaseHandler
from utils import common

class Handle(BaseHandler):
    def initialize(self):
        pass

    def get(self):
        self.redirect('/templates/login.html')