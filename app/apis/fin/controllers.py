from app import db
import math
import pandas as pd
from ...models import Offering, Revenue, Expense
from ..helpers import to_json_res
import datetime
from sqlalchemy.sql import func
from sqlalchemy import or_


def get_offerings():
    offerings = []
    for offering in Offering.query.all():
        offerings.append(offering.to_json2())
    return to_json_res(offerings)


def nan_value_to_empty_string(value):
    return value if not pd.isnull(value) else ''


def reset_db():
    db.drop_all()
    db.create_all()


def get_fin_summary():
    totalOffering = db.session.query(func.sum(Offering.amount)).scalar()
    totalExpense = db.session.query(func.sum(Expense.amount)).scalar()
    totalRevenue = db.session.query(func.sum(Revenue.amount)).scalar()

    totalMissionaryOffering = db.session.query(func.sum(Offering.amount)).filter(
        Offering.category == '선교헌금'
    ).scalar()
    totalMissionaryExpense = db.session.query(func.sum(Expense.amount)).filter(
        Expense.team == '전도사역'
    ).scalar()
    
    totalVehicleOffering = db.session.query(func.sum(Offering.amount)).filter(
        Offering.category == '차량헌금'
    ).scalar()

    totalConstructionOffering = db.session.query(func.sum(Offering.amount)).filter(
        Offering.category == '건축헌금'
    ).scalar()
    return {
        'totalAmount': totalOffering - totalExpense + totalRevenue,
        'totalMissionaryOffering': totalMissionaryOffering - totalMissionaryExpense,
        'totalVehicleOffering': totalVehicleOffering,
        'totalConstructionOffering': totalConstructionOffering,
    }


def get_finance_data(year):
    start_date = datetime.datetime.strptime(
        '01-01-' + year + ' 00:00:00', '%m-%d-%Y %H:%M:%S')
    end_date = datetime.datetime.strptime(
        '12-31-' + year + ' 23:59:59', '%m-%d-%Y %H:%M:%S')

    totalGeneralOffering = 0
    offerings = []
    for offering in Offering.query.filter(
        Offering.date >= start_date,
        Offering.date <= end_date,
    ):
        offerings.append(offering.to_json2())
        if (offering.category in ['주일헌금', '감사헌금', '십일조']):
            totalGeneralOffering += offering.amount

    expenses = []
    for expense in Expense.query.filter(
        Expense.date >= start_date,
        Expense.date <= end_date,
    ):
        expenses.append(expense.to_json2())

    revenues = []
    for revenue in Revenue.query.filter(
        Revenue.date >= start_date,
        Revenue.date <= end_date,
    ):
        revenues.append(revenue.to_json2())

    return {
        'offerings': offerings,
        'expenses': expenses,
        'revenues': revenues,
        'totalGeneralOffering': totalGeneralOffering,
    }


def fetch_fin_data():
    reset_db()
    db_strings = [
        'C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2019 DB.xlsx',
        'C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2020 DB.xlsx',
    ]

    for db_string in db_strings:
        fin_data = pd.read_excel(db_string)

        dateCol = fin_data['Date']
        nameCol = fin_data['Name']
        categoryCol = fin_data['Category']
        typeCol = fin_data['Type']
        amountCol = fin_data['Amount']
        revenueCol = fin_data['Revenue']
        expenseCol = fin_data['Expense']
        statusCol = fin_data['Status']
        if '2020' in db_string:
            teamCol = fin_data['Team']
        else:
            teamCol = fin_data['Department']
        descriptionCol = fin_data['Description']
        typeCol = fin_data['Type']
        referenceCol = fin_data['Reference']
        
        totalIncome = 0
        totalExpense = 0
        total십일조 = 0
        total주일헌금 = 0
        total감사헌금 = 0

        for i in fin_data.index:
            date = dateCol[i]
            amount = amountCol[i]
            revenue = revenueCol[i]
            expense = expenseCol[i]
            status = statusCol[i]
            category = categoryCol[i]
            name = nameCol[i]
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
                
                if (name == '전년이기' and '2019' in db_string) or name != '전년이기':
                    db.session.add( 
                        Offering(
                            date=date if not pd.isnull(date) else None,
                            amount=amount,
                            description=nan_value_to_empty_string(description),
                            name=nan_value_to_empty_string(name),
                            category=nan_value_to_empty_string(category),
                            moneyType=nan_value_to_empty_string(moneyType), 
                        ))

            if not math.isnan(revenue):
                totalIncome += revenue
                db.session.add(
                    Revenue(
                        date=date if not pd.isnull(date) else None,
                        amount=nan_value_to_empty_string(revenue),
                        description=nan_value_to_empty_string(description),
                        team=nan_value_to_empty_string(team),
                        reference=nan_value_to_empty_string(reference),
                    ))
                
            if not math.isnan(expense):
                if status != 'No':
                    totalExpense += expense
                db.session.add(
                    Expense(
                        date=date if not pd.isnull(date) else None,
                        amount=nan_value_to_empty_string(expense),
                        description=nan_value_to_empty_string(description),
                        team=nan_value_to_empty_string(team),
                        status=nan_value_to_empty_string(status),
                        reference=nan_value_to_empty_string(reference),
                    ))
                
    db.session.commit()

    print('노회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.015))
    print('총회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.005))
    print('total income: ${:,.2f}'.format(totalIncome))
    print('total expense: ${:,.2f}'.format(totalExpense))
    print('available balance: ${:,.2f}'.format(totalIncome - totalExpense))
    