''' Import packages start '''
import csv
from openpyxl import Workbook
from openpyxl import load_workbook
''' import packages end '''

''' Initial settings start '''
row_format = '{:<5} {:50} {:<12} {:12} {:<12} {:<14} {:<14} {:<12}'
''' Initial settings end '''

''' DEBUG SETTINGS '''
debug = "N/a"
''' DEBUG SETTINGS END '''

''' Constructor class for fund start '''
class Fund:
    def __init__(self, key, date, fund_name, units, price, book_price, total_cost, value, gain):
        self.k = key
        self.d = date
        self.f = fund_name
        self.u = units
        self.p = price
        self.bp = book_price
        self.tc = total_cost
        self.v = value
        self.g = gain
        self.t = []
        self.converted = 0

        if self.tc == None:
            self.tc = 0

        if self.bp == None:
            self.bp = 0

    def dump(self):
        print([self.k, self.d, self.f, self.u, self.p, self.bp, self.tc, self.v, self.g])
    
    def buy(self, units, price, value, transaction):
        self.u = self.u + units
        self.tc = self.tc + value
        self.bp = self.tc / self.u
        self.t.append(transaction)
        write_me(self.f + ': Bought ' + str(units) + ' units for ' + str(price) + ' per unit')
        if(self.k == debug):
            print(self.f + ': Bought ' + str(units) + ' units for ' + str(price) + ' per unit')
            print('New Book Price: ' + str(self.bp))
            print('New Units: ' + str(self.u))
            print('')
    
    def sell(self, units, price, value, transaction):
        self.u = self.u - units
        self.tc = self.u * self.bp
        self.t.append(transaction)
        write_me(self.f + ': Sold ' + str(units) + ' units for ' + str(price) + ' per unit')
        if(self.k == debug):
            print(self.f + ': Sold ' + str(units) + ' units for ' + str(price) + ' per unit')#
            print('New Book Price: ' + str(self.bp))
            print('New Units: ' + str(self.u))
            print('')

    def convert_in(self, fund, units, price, value, transaction):
        c_format = '£{:,.2f}'
        p_format = '£{:.4f}'
        self.u = self.u + units
        self.tc = self.converted
        self.bp = self.tc / self.u
        self.t.append(transaction)
        self.f = fund
        write_me(self.f + ': Converted in ' + str(units) + ' units with a book cost of ' + str(c_format.format(self.tc)) + ' and a new avg. price of ' + p_format.format(self.bp))
        if(self.k == debug):
            print(self.f + ': Converted in ' + str(units) + ' units with a book cost of ' + str(c_format.format(self.tc)) + ' and a new avg. price of ' + p_format.format(self.bp))
            print('New Book Price: ' + str(self.bp))
            print('New Units: ' + str(self.u))
            print('')
    
    def convert_out(self, units, price, value, transaction):
        c_format = '£{:,.2f}'
        self.u = self.u - units
        self.converted = self.tc
        self.t.append(transaction)
        write_me(self.f + ': Converted out ' + str(units) + ' units with a book cost of ' + str(c_format.format(self.converted)))
        if(self.k == debug):
            print(self.f + ': Converted out ' + str(units) + ' units with a book cost of ' + str(c_format.format(self.converted)))
            print('New Book Price: ' + str(self.bp))
            print('New Units: ' + str(self.u))
            print('')
    
    def fund_info(self):
        p_format = '£{:.4f}'
        n_format = '{:.4f}'
        c_format = '£{:,.2f}'
        #row_format = '{:<5} {:15} {:<8} {:12} {:<12} {:<10} {:<10} {:<10}'
        self.info = [self.k, self.f, n_format.format(self.u), p_format.format(self.p), p_format.format(self.bp), c_format.format(self.tc), c_format.format(self.v), c_format.format(self.g)]
        return(row_format.format(*self.info))

    def headers(self):
        #row_format = '{:<5} {:15} {:<8} {:12} {:<12} {:<10} {:<10} {:<10}'
        return(row_format.format(*['Key', 'Fund Name', 'Units', 'Price', 'Book Price', 'Book Cost', 'Value', 'Growth']))
    
    def add_valuation(self, date, fund, units, price):
        self.d = date
        self.f = fund
        self.p = price
        self.v = units * self.u
        self.tc = self.u * self.bp

''' Construct class for fund end '''

''' Custom functions start ''' 
def write_me(data):
    output_me.write(data)
    output_me.write('\n')
''' Custom functions end '''

''' Main start '''
# Settings
csv_file = 'data.csv'
excel_file = 'Data.xlsx'
output_file = 'output.txt'

# Lists set up for holding fund info
current_fund = []
fund_list = []
fund_store = []

# List set up for holding transaction info
current_transaction = []
transaction_list = []
transaction_store = []

# Storage for the totals
t_value = 0
t_cost = 0
t_gain = 0

# Loads output file for working with
output_me = open(output_file, 'a')

# Loads workbook into variable
wb = load_workbook(excel_file, data_only=True)

# Stores list of sheet names should they change in future
sheet_names = wb.get_sheet_names()

# Valuation sheet should always be first sheet & Transactions the second
ws_valuation = wb.get_sheet_by_name(sheet_names[0])
ws_transactions = wb.get_sheet_by_name(sheet_names[1])
ws_final_value = wb.get_sheet_by_name(sheet_names[2])

# Loops through all funds and creates a nested list based on excel data (ROWS on line 0)
for i, rows in enumerate(ws_valuation, start=0):
    current_fund = []
    for cell in rows:
        current_fund.append(cell.value)
    fund_list.append(current_fund)

# Loops through funds in nested list and creates list of objects
for i, rows in enumerate(fund_list, start=0):
    if(fund_list[i][0] == None):
        pass
    else:
        curfund = Fund(fund_list[i][0],fund_list[i][1],fund_list[i][2],fund_list[i][3],fund_list[i][4],fund_list[i][5],fund_list[i][6],fund_list[i][7],fund_list[i][8])
        fund_store.append(curfund)

# Deletes first fund as this is where headers are stored
del fund_store[0]

# Test to display all funds in list
print('Starting valuation')
print(fund_store[0].headers())
write_me(fund_store[0].headers())
for funds in fund_store:
    print(funds.fund_info())
    write_me(funds.fund_info())
print('')

print('Transactions')

# Loop through all transactions and output to a list
for i, rows in enumerate(ws_transactions, start=0):
    current_transaction = []
    for cell in rows:
        current_transaction.append(cell.value)
    transaction_list.append(current_transaction)

# Loop through all transactions in list and add to the funds
print('Transactions')

''' LOOPS THROUGH ALL TRANSACTIONS '''

for i, row in enumerate(transaction_list, start=0):
    if i == 0:
        pass
    else:
        cur_fund = Fund(row[0], row[1], row[2], row[4], row[5], row[5], row[6], row[6], 0)
        NEW_FUND = True
        # Check all funds in the current fund list
        for f, fund in enumerate(fund_store, start=0):
            if(NEW_FUND == True):
                if(fund.k == cur_fund.k):
                    NEW_FUND = False
                    # DO X if fund is in list
                    if(transaction_list[i][3] == 'Buy'):
                        # DO X if transaction is a buy
                        fund.buy(row[4], row[5], row[6], row)
                    if(transaction_list[i][3] == 'Sell'):
                        # DO X if transaction is a sell
                        fund.sell(row[4], row[5], row[6], row)
                    if(transaction_list[i][3] == 'Convert in'):
                        # DO X if transaction is a conversion in
                        fund.convert_in(row[2], row[4], row[5], row[6], row)
                    if(transaction_list[i][3] == 'Convert out'):
                        # DO X if transaction is a conversion out
                        fund.convert_out(row[4], row[5], row[6], row)
                else:
                    # DO X if fund not already on list
                    pass
            else:
                # Do X if fund has been found already
                pass
        if(NEW_FUND == True):
            fund_store.append(cur_fund)
            write_me(cur_fund.f + ' - fund added')
            if(cur_fund.k == debug):
                print(cur_fund.f + ' - fund added')

print('\n' + '#####DEBUG#####')
print(transaction_store)
print('#####DEBUG#####' + '\n')

''' FINISH LOOPING THROUGH TRANSACTIONS '''

''' ADD FINAL VALUATION FIGURES '''

current_fund = []
fund_list = []

for i, rows in enumerate(ws_final_value, start=0):
    current_fund = []
    for cell in rows:
        current_fund.append(cell.value)
    fund_list.append(current_fund)
    
for i, rows in enumerate(fund_list, start=0):
    if(fund_list[i][0] == None):
        pass
    else:
        cur_fund = Fund(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8])
        for f, fund in enumerate(fund_store, start=0):
            if(fund.k == cur_fund.k):
                fund.v = cur_fund.v
                fund.f = cur_fund.f
                fund.d = cur_fund.d
            else:
                pass

''' FINISH ADDING FINAL VALUATION FIGURES '''


# Print funds for test - new values
write_me('\n')
write_me('Ending Valuation')
write_me(fund_store[0].headers())

# Add up totals for bottom line and print each line of stock with a value
for funds in fund_store:
    if funds.u != 0:
        print(funds.fund_info())
        write_me(funds.fund_info())
        t_value += funds.v
        t_cost += funds.tc
        t_gain += funds.g
print(row_format.format(*['Total', '', '', '', '', '£{:,.2f}'.format(t_cost), '£{:,.2f}'.format(t_value), '£{:,.2f}'.format(t_gain)]))
write_me(row_format.format(*['Total', '', '', '', '', '£{:,.2f}'.format(t_cost), '£{:,.2f}'.format(t_value), '£{:,.2f}'.format(t_gain)]))

# Export text closed
output_me.close()
''' Main end '''