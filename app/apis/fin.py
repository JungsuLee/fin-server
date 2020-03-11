from flask_restplus import Namespace, Resource, reqparse
import pandas as pd
import math

api = Namespace('fin')

@api.route('')
class FinApi(Resource):
    def get(self):
        return get_2020_fins()



def get_2020_fins():
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
    refereenceCol = db2020['Reference']
    
    fins = []
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
        refereence = refereenceCol[i]
        
        if not math.isnan(amount):
            totalIncome += amount
            if category == '주일헌금':
                total주일헌금 += amount
            if category == '감사헌금':
                total감사헌금 += amount
            if category == '십일조':
                total십일조 += amount
            fins.append({
                # 'date': date,
                'amount': amount,
                'description': description,
                'type': 'offering',
                
                'name': name,
                'category': category,
                'moneyType': moneyType,
            })

        if not math.isnan(revenue):
            totalIncome += revenue
            fins.append({
                # 'date': date,
                'amount': revenue,
                'description': description,
                'type': 'revenue',
                
                'ministry': ministry,
                'team': team,
                'reference': refereence,
            })
            
        if not math.isnan(expense):
            if status != 'No':
                totalExpense += expense
            fins.append({
                # 'date': date,
                'amount': expense,
                'description': description,
                'type': 'expense',
                
                'ministry': ministry,
                'team': team,
                'status': status,
            })

    print('노회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.015))
    print('총회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.005))
    print('total income: ${:,.2f}'.format(totalIncome))
    print('total expense: ${:,.2f}'.format(totalExpense))
    print('available balance: ${:,.2f}'.format(totalIncome - totalExpense))
    return fins
