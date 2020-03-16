from flask_restplus import Namespace, Resource, reqparse
from app import db


api = Namespace('db')

@api.route('/drop-all')
class DropAllApi(Resource):
    def get(self):
        return db.drop_all()


@api.route('/create-all')
class CreateAllApi(Resource):
    def get(self):
        return db.create_all()
