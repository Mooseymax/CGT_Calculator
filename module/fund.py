from datetime import datetime, timedelta

class Fund:
    def __init__(self, key, date, fund_name, units, price, book_price, book_cost, value, gain):
        self.k = key            # Unique reference
        self.d = date           # Initial date purchased
        self.f = fund_name      # Fund name
        self.u = units          # Current units
        self.p = price          # Current price
        self.bp = book_price    # Book cost / units
        self.bc = book_cost     # Book cost
        self.v = value          # Current value
        self.g = gain           # Overall gain -> value - book cost
        self.t = []             # List of ALL transactions
        
        ''' 50 unit Buy on 01/01
            50 unit Buy on 01/05
            40 unit Sell on 02/05
            Remove 40 units from 30 day pool
            50 units from 01/01
            10 units from 01/05
            All will then go into the S104 pool after 30 days
            
            Alternative:
            60 unit Sell on 02/05
            Remove 50 units from 30 day pool
            40 units from 01/01
            All in the S104 pool as 30 day pool gone
            
            Alternative 2:
            50 unit Buy on 01/01
            40 unit Sell on 01/05
            50 unit Buy on 02/05
            Remove 40 units from 30 day pool
            50 units from 01/01
            10 units from 02/05
            All will then go into the S104 pool after 30 days'''
        
        self.t_pool = T_Pool()  # Transactions split between 0, 30 & 104
        
        if self.bc == None:
            self.bc = 0
        
        if self.bp == None:
            self.bp = 0
    
    # Function to realign all previous transactions based on latest transaction
    def update_tran(self, transaction):
        # 0 / 30 / 104 rule check
        for transactions in self.t:
            
            if t.compare(transaction) == 0:
                # Do if zero day
            elif t.compare(transaction) == 30:
                # Do if 30 day
            else:
                # Do if Section 104
    
    def tranact(self, transaction):
        t = transaction
        if t.t == 'Buy':
            self.buy(t)
        elif t.t == 'Sell':
            self.sell(t)
        elif t.t == 'Convert in':
            self.convert_in(t)
        elif t.t == 'Convert out':
            self.convert_out(t)
        elif t.t == 'Transfer in':
            self.transfer_in(t)
        elif t.t == 'Transfer out':
            self.transfer_out(t)
        elif t.t == 'Distribution':
            self.distribution(t)
        elif t.t == 'Equalisation':
            self.equalisation(t)
        
    def buy(self, transaction):
        t = transaction
        day_a = []  # Same day trades
        day_b = []  # 30 day trades
        day_x = []  # 104 trades
        
        # Check and split transactions into separate groups
        for transactions in self.t:
            if t.compare(transaction) == 0:
                day_a.append(transaction)
            elif t.compare(transaction) == 30:
                day_b.append(transaction)
            else:
                day_x.append(transaction)

class T_Pool:
    def __init__(self):
        self.a = [] # Same day trades
        self.b = [] # 30 day trades
        self.x = [] # 104 trades
        
class Transaction:
    def __init__(self, transaction):
        self.d = transaction[0] # Date
        self.f = transaction[1] # Fund name
        self.t = transaction[2] # Type of transaction
        self.u = transaction[3] # Units
        self.p = transaction[4] # Price
        self.v = transaction[5] # Value
        
        if self.v == None:
            self.v = self.u * self.p    # Value bought
    
    def compare(self, external_transaction):
        t = external_transaction
        delta_time = self.d - t.d
        
        if delta_time.days == 0:
            return 0
        elif delta_time.days > 0 and delta_time.days <= 30:
            return 30
        else:
            return 104
