from app import db
import pandas as pd
from ...models import Finance
import math


def reset_db():
    db.drop_all()
    db.create_all()


def nan_value_to_empty_string(value):
    return value if not pd.isnull(value) else ''


def fetch_fin_data():
    reset_db()
    db_strings = [
        "C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2015년도\\15년도 DB.xlsx",
        "C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2016년도\\16년도 DB.xls",
        "C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2017년도\\17년도 DB.xls",
        "C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2018년도\\18년도 DB.xls",
        'C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2019 DB.xlsx',
        'C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2020 DB.xlsx',
    ]

    for db_string in db_strings:
        fin_data = pd.read_excel(db_string)

        dateCol = fin_data['Date']
        amountCol = fin_data['Amount']
        categoryCol = fin_data['Category']
        revenueCol = fin_data['Revenue']
        expenseCol = fin_data['Expense']
        if '2020' in db_string:
            teamCol = fin_data['Team']
        else:
            teamCol = fin_data['Department']
        descriptionCol = fin_data['Description']
        
        nameCol = fin_data['Name']
        # typeCol = fin_data['Type']
        # statusCol = fin_data['Status']
        # referenceCol = fin_data['Reference']

        for i in fin_data.index:
            date = dateCol[i]
            amount = amountCol[i]
            revenue = revenueCol[i]
            expense = expenseCol[i]
            category = categoryCol[i]
            team = teamCol[i]
            description = descriptionCol[i]
            
            name = nameCol[i]
            # moneyType = typeCol[i]
            # reference = referenceCol[i]
            # status = statusCol[i]
            
            if not math.isnan(amount):
                if ('전년이기' in name and '2015' in db_string) or name != '전년이기':
                    db.session.add(
                        Finance(
                            date=date if not pd.isnull(date) else None,
                            category=nan_value_to_empty_string(category),
                            amount=nan_value_to_empty_string(amount),
                            description=nan_value_to_empty_string(description),
                            type='offering'
                        )
                    )
            if not math.isnan(revenue):
                db.session.add(
                    Finance(
                        date=date if not pd.isnull(date) else None,
                        category=nan_value_to_empty_string(team),
                        amount=nan_value_to_empty_string(revenue),
                        description=nan_value_to_empty_string(description),
                        type='revenue'
                    )
                )
            if not math.isnan(expense):
                db.session.add(
                    Finance(
                        date=date if not pd.isnull(date) else None,
                        category=nan_value_to_empty_string(team),
                        amount=nan_value_to_empty_string(expense),
                        description=nan_value_to_empty_string(description),
                        type='expense'
                    )
                )
    db.session.commit()
