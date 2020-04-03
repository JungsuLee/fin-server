from flask_restplus import Namespace, Resource
from . import controllers


api = Namespace('analytics')


@api.route('/<year>')
@api.param('year')
class FinanceDataApi(Resource):
    def get(self, year):
        return controllers.get_analytics(year)
