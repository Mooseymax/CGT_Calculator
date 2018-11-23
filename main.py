import csv
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl import load_workbook
from module.fund import Fund, Transaction, T_Pool

today = datetime.today()
example_name = 'Fund A'

example_fund = Fund(1, today, example_name, 100, 1, 1, 100, 100)

if example_fund.f == example_name:
    print('1. Working')

example_transaction = Transaction([today + timedelta(days=40), 'Fund A2', 'Buy', 100, 2, 200])

example_fund.transact(example_transaction)

print('DEBUG: ' + example_fund.f)
print('DEBUG: ' + str(example_fund.u))
print('2. Working')