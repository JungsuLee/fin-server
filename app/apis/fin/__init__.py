from flask_restplus import Namespace, Resource
from ...models import Offering, Revenue, Expense
from . import controllers


api = Namespace('fin')


@api.route('/fetch')
class FetchFinDataApi(Resource):
    def get(self):
        return controllers.fetch_fin_data()


@api.route('/offerings')
class OfferingsApi(Resource):
    def get(self):
        return controllers.get_offerings()


@api.route('/data/<year>')
@api.param('year')
class FinanceDataApi(Resource):
    def get(self, year):
        return controllers.get_finance_data(year)


@api.route('/summary')
class FinanceSummaryApi(Resource):
    def get(self):
        return controllers.get_fin_summary()
