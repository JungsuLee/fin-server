from flask_restplus import Namespace, Resource
from app import db
from ..models import Offering, Revenue, Expense
import math
import pandas as pd
from .helpers import to_json_res


api = Namespace('fin')



@api.route('')
class FinApi(Resource):
    def get(self):
        fins = get_2020_fins()
        return to_json_res(fins)


@api.route('/fetch')
class FetchFinDataApi(Resource):
    def get(self):
        return get_2020_fins()


@api.route('/offerings')
class OfferingsApi(Resource):
    def get(self):
        offerings = []
        for offering in Offering.query.all():
            offerings.append(offering_to_json(offering))
        return to_json_res(offerings)
        # return jsonify(offerings)


def offering_to_json(offering):
    return {
        'date': str(offering.date),
        'amount': offering.amount,
        'description': offering.description,
        'name': offering.name,
        'category': offering.category,
        'moneyType': offering.moneyType,
    }


def get_2020_fins():
    db.drop_all()
    db.create_all()
    db2020 = pd.read_excel('C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2020 DB.xlsx')    
    dateCol = db2020['Date']
    nameCol = db2020['Name']
    categoryCol = db2020['Category']
    typeCol = db2020['Type']
    amountCol = db2020['Amount']
    revenueCol = db2020['Revenue']
    expenseCol = db2020['Expense']
    statusCol = db2020['Status']
    ministryCol = db2020['Ministry']
    teamCol = db2020['Team']
    descriptionCol = db2020['Description']
    typeCol = db2020['Type']
    referenceCol = db2020['Reference']
    
    offerings = []
    revenues = []
    expenses = []
    totalIncome = 0
    totalExpense = 0
    total십일조 = 0
    total주일헌금 = 0
    total감사헌금 = 0
    for i in db2020.index:
        date = dateCol[i]
        amount = amountCol[i]
        revenue = revenueCol[i]
        expense = expenseCol[i]
        status = statusCol[i]
        category = categoryCol[i]
        name = nameCol[i]
        ministry = ministryCol[i]
        team = teamCol[i]
        description = descriptionCol[i]
        moneyType = typeCol[i]
        reference = referenceCol[i]
        
        if not math.isnan(amount):
            totalIncome += amount
            if category == '주일헌금':
                total주일헌금 += amount
            if category == '감사헌금':
                total감사헌금 += amount
            if category == '십일조':
                total십일조 += amount
            # offering = {
            #     'date': date,
            #     'amount': amount,
            #     'description': description,
            #     'name': name,
            #     'category': category,
            #     'moneyType': moneyType,
            # }
            db.session.add( 
                Offering(
                    date=date if not pd.isnull(date) else None,
                    amount=amount,
                    description=description,
                    name=name,
                    category=category,
                    moneyType=moneyType, 
                ))
            # db.session.commit()
            # offerings.append(offering)
            # if pd.isnull(date):
            #     print(name)

        if not math.isnan(revenue):
            totalIncome += revenue
            # revenue = {
            #     'date': date,
            #     'amount': revenue,
            #     'description': description,
            #     'ministry': ministry,
            #     'team': team,
            #     'reference': reference,
            # }
            db.session.add(
                Revenue(
                    date=date,
                    amount=revenue,
                    description=description,
                    ministry=ministry,
                    team=team,
                    reference=reference,
                ))
            # db.session.commit()
            # revenues.append(revenue)
            
        if not math.isnan(expense):
            if status != 'No':
                totalExpense += expense
            # expense = {
            #     'date': date,
            #     'amount': expense,
            #     'description': description,
            #     'ministry': ministry,
            #     'team': team,
            #     'status': status,
            #     'reference': reference,
            # }
            db.session.add(
                Expense(
                    date=date,
                    amount=expense,
                    description=description,
                    ministry=ministry,
                    team=team,
                    status=status,
                    reference=reference,
                ))
            # db.session.commit()
            # expenses.append(expense)
    db.session.commit()

    print('노회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.015))
    print('총회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.005))
    print('total income: ${:,.2f}'.format(totalIncome))
    print('total expense: ${:,.2f}'.format(totalExpense))
    print('available balance: ${:,.2f}'.format(totalIncome - totalExpense))
    
    return {
        'offerings': offerings,
        'expenses': expenses,
        'revenues': revenues,
    }
