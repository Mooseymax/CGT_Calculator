import csv
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl import load_workbook
from module.fund import Fund, Transaction, T_Pool

today = datetime.today()
example_name = 'Fund A'

fund_a = Fund(1, today - timedelta(days=40), example_name, 100, 1, 1, 100, 100)
print('DEBUG: Initial units are ' + str(fund_a.u))

if fund_a.f == example_name:
    print('1. Working')

transaction_a = Transaction([today, 'Fund A', 'Buy', 1000, 1, 1000])
transaction_b = Transaction([today + timedelta(days=40), 'Fund A1', 'Sell', 400, 1.1, 550])
transaction_c = Transaction([today + timedelta(days=41), 'Fund A1', 'Buy', 500, 1.2, 120])
# transaction_d = Transaction([today + timedelta(days=42), 'Fund A1', 'Buy', 500, 1.3, 120])

transaction_list = [transaction_a,transaction_b,transaction_c]

for t in transaction_list:
    fund_a.transact(t)
    print(' ')

print(fund_a.f)
print(fund_a.u)
print(fund_a.bc)