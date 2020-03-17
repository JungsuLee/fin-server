from app import db
import math
import pandas as pd
from ...models import Offering, Revenue, Expense
from ..helpers import to_json_res


def get_offerings():
    offerings = []
    for offering in Offering.query.all():
        offerings.append(offering.to_json2())
    return to_json_res(offerings)


def nan_value_to_empty_string(value):
    return value if not pd.isnull(value) else ''


def fetch_fin_data():
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
    