from flask_restplus import Api
from .fin import api as fin


api = Api()

api.add_namespace(fin, path='/fin')