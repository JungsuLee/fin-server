import pandas as pd
import math


db2020 = pd.read_excel('C:\\Users\\ljs96\\Dropbox\\재정 Finances\\2020 DB.xlsx')

print(db2020.columns)
amountCol = db2020['Amount']
revenueCol = db2020['Revenue']
expenseCol = db2020['Expense']
statusCol = db2020['Status']
categoryCol = db2020['Category']

totalIncome = 0
totalExpense = 0
total십일조 = 0
total주일헌금 = 0
total감사헌금 = 0

for i in db2020.index:
    amount = amountCol[i]
    revenue = revenueCol[i]
    expense = expenseCol[i]
    status = statusCol[i]
    
    if not math.isnan(amount):
        totalIncome += amount
        if categoryCol[i] == '주일헌금':
            total주일헌금 += amount
        if categoryCol[i] == '감사헌금':
            total감사헌금 += amount
        if categoryCol[i] == '십일조':
            total십일조 += amount

    if not math.isnan(revenue):
        totalIncome += revenue
    if not math.isnan(expense) and status != 'No':
        totalExpense += expense

print('노회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.015))
print('총회 상회비: ${:,.2f}'.format((total주일헌금 + total감사헌금 + total십일조) * 0.005))

print('total income: ${:,.2f}'.format(totalIncome))
print('total expense: ${:,.2f}'.format(totalExpense))  

print('available balance: ${:,.2f}'.format(totalIncome - totalExpense))



