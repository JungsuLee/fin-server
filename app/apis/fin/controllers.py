from app import db
from ...models import Finance
import datetime
from sqlalchemy.sql import func


def get_fin_summary():
    totalOffering = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.type == 'offering'
        ).scalar()
    totalExpense = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.type == 'expense'
        ).scalar()
    totalRevenue = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.type == 'revenue'
        ).scalar()
    totalMissionaryOffering = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '선교헌금'
    ).scalar()
    totalMissionaryExpense = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '전도사역'
    ).scalar()
    totalVehicleOffering = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '차량헌금'
    ).scalar()
    totalVehicleExpense = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '차량 지정',
        Finance.type == 'expense',
    ).scalar()
    totalConstructionOffering = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '건축헌금'
    ).scalar()
    totalConstructionExpense = db.session.query(
        func.sum(Finance.amount)).filter(
        Finance.category == '건축사역',
        Finance.type == 'expense',
    ).scalar()
    return {
        'totalAmount': totalOffering - totalExpense + totalRevenue,
        'totalMissionaryOffering': totalMissionaryOffering - totalMissionaryExpense,
        'totalVehicleOffering': totalVehicleOffering - totalVehicleExpense,
        'totalConstructionOffering': totalConstructionOffering - totalConstructionExpense,
    }


def get_finance_data(year):
    start_date = datetime.datetime.strptime(
        '01-01-' + year + ' 00:00:00', '%m-%d-%Y %H:%M:%S')
    end_date = datetime.datetime.strptime(
        '12-31-' + year + ' 23:59:59', '%m-%d-%Y %H:%M:%S')

    totalGeneralOffering = 0
    totalSpecialOffering = 0
    offerings = []
    for offering in db.session.query(
        Finance.date,
        Finance.category,
        func.sum(Finance.amount),
    ).filter(
        Finance.date >= start_date,
        Finance.date <= end_date,
        Finance.type == 'offering'
    ).group_by(
        Finance.date, 
        Finance.category
    ).order_by(Finance.date).all():
        offerings.append({
            'date': offering[0].strftime('%m/%d'),
            'category': offering[1],
            'amount': offering[2],
        })
        if (offering[1] in ['주일헌금', '감사헌금', '십일조']):
            totalGeneralOffering += offering[2]
        else:
            totalSpecialOffering += offering[2]

    expenses = []
    totalExpense = 0
    for expense in Finance.query.filter(
        Finance.date >= start_date,
        Finance.date <= end_date,
        Finance.type == 'expense',
    ):
        expenseJson = expense.to_json2()
        expenses.append(expenseJson)
        totalExpense += expenseJson['amount']

    revenues = []
    totalRevenue = 0
    for revenue in Finance.query.filter(
        Finance.date >= start_date,
        Finance.date <= end_date,
        Finance.type == 'revenue',
    ):
        revenueJson = revenue.to_json2()
        revenues.append(revenueJson)
        totalRevenue += revenueJson['amount']

    return {
        'offerings': offerings,
        'expenses': expenses,
        'revenues': revenues,
        'totalGeneralOffering': totalGeneralOffering,
        'totalSpecialOffering': totalSpecialOffering,
        'totalExpense': totalExpense,
        'totalRevenue': totalRevenue,
    }
    