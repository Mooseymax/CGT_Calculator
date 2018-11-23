from datetime import datetime, timedelta

class Fund:
    def __init__(self, key, date, fund_name, units, price, book_price, book_cost, value):
        self.k = key            # Unique reference
        self.d = date           # Initial date purchased
        self.f = fund_name      # Fund name
        self.u = units          # Current units
        self.p = price          # Current price
        self.bp = book_price    # Book cost / units
        self.bc = book_cost     # Book cost
        self.v = value          # Current value
        self.g = 0              # Overall gain -> value - book cost
        self.t = [Transaction([self.d, self.f, 'Initial', self.u, self.p, self.v])]             # List of ALL transactions
        
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
        self.t_pool.a = []  # Same day trades
        self.t_pool.b = []  # 30 day trades
        self.t_pool.x = []  # 104 trades
        
        # 0 / 30 / 104 rule check
        for t in self.t:
            print('DEBUG: ' + t.f)
            if t.compare(transaction) == 0:
                # Do if 0 day
                print('DEBUG: Day 0')
                self.t_pool.a.append(transaction)
            elif t.compare(transaction) == 30:
                # Do if 30 day
                self.t_pool.b.append(transaction)
            else:
                # Do if Section 104
                self.t_pool.x.append(transaction)
    
    def transact(self, transaction):
        t = transaction
        if t.t == 'Buy':
            print('DEBUG: Buy')
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
        print('DEBUG: ' + t.f)
        
        # Check and split transactions into separate groups
        self.update_tran(t)
        
        ''' Loop through to check if matches against any existing pools '''
        # Do if 0 day not empty and all units not yet matched
        if self.t_pool.a and not t.check_matched():
            print('DEBUG: Inside Day 0')
            for tran_a in self.t_pool.a:
                t.matched += tran_a.u
                print("Day 0 rule triggered")
                if t.check_matched():
                    break
        # Do if 30 day not empty and all units not yet matched
        elif self.t_pool.b and not t.check_matched():
            for tran_b in self.t_pool.b:
                t.matched += tran_b.u
                print("Day 30 rule triggered")
                if t.check_matched():
                    break
        # Do if S104 not empty and all units not yet matched
        elif self.t_pool.x and not t.check_matched():
            for tran_x in self.t_pool.x:
                t.matched += tran_x.u        # Use units in this pool
                self.u += t.u                   # Add units to fund
                self.bc += t.v                  # Add cost of purchase
                self.f = t.f                    # Update fund name (if changed slightly)
                print("Added to Section 104")   # DEBUG
                if t.check_matched():
                    break
        
        # Adds transaction to the list
        self.t.append(transaction)

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
        
        self.matched = 0
        
        if self.v == None:
            self.v = self.u * self.p    # Value bought
    
    # Function to check if matched off against other units in pool
    def check_matched(self):
        if self.u == self.matched:
            return True
        else:
            return False
    
    def compare(self, external_transaction):
        t = external_transaction
        delta_time = self.d - t.d
        
        if delta_time.days == 0:
            return 0
        elif delta_time.days > 0 and delta_time.days <= 30:
            return 30
        else:
            return 104
