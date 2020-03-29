from flask_restplus import Namespace, Resource
from . import controllers
from .fetch import fetch_fin_data


api = Namespace('fin')


@api.route('/fetch')
class FetchFinDataApi(Resource):
    def get(self):
        return fetch_fin_data()


@api.route('/data/<year>')
@api.param('year')
class FinanceDataApi(Resource):
    def get(self, year):
        return controllers.get_finance_data(year)


@api.route('/summary')
class FinanceSummaryApi(Resource):
    def get(self):
        return controllers.get_fin_summary()
