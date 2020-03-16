from flask_restplus import Api
from .fin import api as fin
from .user import api as user
from .db import api as db

api = Api()

api.add_namespace(fin, path='/fin')
api.add_namespace(user, path='/user')
api.add_namespace(db, path='/db')