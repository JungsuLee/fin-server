from flask_restplus import Namespace, Resource, reqparse
from app import db
from ..models import User


api = Namespace('user')

@api.route('')
class UserApi(Resource):
    def get(self):
        return User.query.all()
