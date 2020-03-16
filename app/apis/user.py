from flask_restplus import Namespace, Resource, reqparse
from app import db
from ..models import User


api = Namespace('user')

@api.route('')
class UserApi(Resource):
    def get(self):
        # user = User(username='jung', email='jung@gmail.com')
        # db.session.add(user)
        # db.session.commit()
        return User.query.all()
