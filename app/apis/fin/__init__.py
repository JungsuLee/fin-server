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
