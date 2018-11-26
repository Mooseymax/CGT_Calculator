from datetime import datetime, timedelta

debug_mode = False
logging = True
logging_key = 12

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
        self.t = [Transaction([self.k, self.d, self.f, 'Initial', self.u, self.p, self.v])]             # List of ALL transactions
        
        '''
        50 unit Buy on 01/01
        40 unit Sell on 01/05
        50 unit Buy on 02/05
        Remove 40 units from 30 day pool
        50 units from 01/01
        10 units from 02/05
        All will then go into the S104 pool after 30 days
        '''
        
        self.t_pool = T_Pool()  # Transactions split between 0, 30 & 104
        
        if self.bc == None:
            self.bc = 0
        
        if self.bp == None:
            self.bp = 0
    
    def debug(self):
        print(str(self.k) + ' ' + self.f + ' ' + str(self.u))
    
    # Function to realign all previous transactions based on latest transaction
    def update_tran(self, transaction):
        self.t_pool.a = []  # Same day trades
        self.t_pool.b = []  # 30 day trades
        self.t_pool.x = []  # 104 trades
        
        current_t = transaction
        
        # 0 / 30 / 104 rule check
        for t in self.t:
            if t.compare(current_t) == 0 and t.t == 'Sell':
                # Do if 0 day
                self.t_pool.a.append(t)
            elif t.compare(current_t) == 30 and t.t == 'Sell':
                # Do if 30 day
                self.t_pool.b.append(t)
            else:
                # Do if Section 104
                self.t_pool.x.append(t)
        
        if debug_mode:
            print('DEBUG: Updated transactions')
    
    def transact(self, transaction):
        current_t = transaction
        if current_t.t == 'Buy':
            if debug_mode:
                print('DEBUG: Buy')
            self.buy(current_t)
        elif current_t.t == 'Sell':
            if debug_mode:
                print('DEBUG: Sell')
            self.sell(current_t)
        elif current_t.t == 'Convert in':
            self.convert_in(current_t)
        elif current_t.t == 'Convert out':
            self.convert_out(current_t)
        elif current_t.t == 'Transfer in':
            self.transfer_in(current_t)
        elif current_t.t == 'Transfer out':
            self.transfer_out(current_t)
        elif current_t.t == 'Distribution':
            self.distribution(current_t)
        elif current_t.t == 'Equalisation':
            self.equalisation(current_t)
    
    ''' BUY TRANSACTION SECTION '''
    def buy(self, transaction):
        current_t = transaction
        if debug_mode:
            print('DEBUG: ' + current_t.f)
        
        # Check and split transactions into separate groups
        self.update_tran(current_t)
        
        # Stores previous averege price of S104 pool
        price = self.bc / self.u
        
        ''' Loop through to check if matches against any existing pools '''
        if self.t_pool.a and not current_t.check_matched():
            # Do if sale placed within 0 days
            if debug_mode:
                print("DEBUG: Matching Day 0 disposals")
            for t in self.t_pool.x:
                # Update matched units
                matched = min(current_t.u, t.u-t.matched)
                current_t.matched += matched
                t.matched += matched
                
                # Add matched units to S104 pool at original price
                self.u += matched
                if matched != 0:
                    self.bc += (matched * price)
                else:
                    self.bc += current_t.v
                self.f = current_t.f
                # Logging for debugging purposes
                if logging and self.k == logging_key:
                    print('LOG: Fund Name = ' + self.f)
                    print('LOG: Matched ' + str(matched) + ' units against 0 day disposals')
                    print('LOG: Current Units = ' + str(self.u))
                    print('LOG: Running Cost = £' + '{:.2f}'.format(self.bc))
                    print('')
                if debug_mode:
                    current_t.debug()
                if current_t.check_matched():
                    if debug_mode:
                        print('DEBUG: All units matched')
                    break
        if self.t_pool.b and not current_t.check_matched():
            # Do if sale placed within 30 days
            if debug_mode:
                print("DEBUG: Matching Day 30 disposals")
            for t in self.t_pool.b:
                # Update matched units
                matched = min(current_t.u, t.u-t.matched)
                current_t.matched += matched
                t. matched += matched
                
                # Add matched units to S104 pool at original price
                self.u += matched
                if matched != 0:
                    self.bc += (matched * price)
                else:
                    self.bc += current_t.v
                self.f = current_t.f
                if logging and self.k == logging_key:
                    print('LOG: Fund Name = ' + self.f)
                    print('LOG: Matched ' + str(matched) + ' units against 30 day disposals')
                    print('LOG: Current Units = ' + str(self.u))
                    print('LOG: Running Cost = £' + '{:.2f}'.format(self.bc))
                    print('')
                if debug_mode:
                    current_t.debug()
                if current_t.check_matched():
                    if debug_mode:
                        print('DEBUG: All units matched')
                    break
        if self.t_pool.x and not current_t.check_matched():
            # Do if units are in the S104 section
            if debug_mode:
                print("DEBUG: Adding remainder to S104")
           
            matched = current_t.u - current_t.matched   # Units left to match
            self.u += matched                           # Adds units left to match to S104
            if matched != 0:
                self.bc += (matched * current_t.p)      # Adds to book cost based on transaction price
            else:
                self.bc += current_t.v
            self.f = current_t.f                        # Updates fund name
            if logging and self.k == logging_key:
                print('LOG: Fund Name = ' + self.f)
                print('LOG: Added ' + str(matched) + ' units to the S104 pool || Price = ' + str(current_t.p))
                print('LOG: Current Units = ' + str(self.u))
                print('LOG: Running Cost = £' + '{:.2f}'.format(self.bc))
                print('')
            if current_t.check_matched():
                if debug_mode:
                    print('DEBUG: All units matched')
            
        if not self.t:
            # Do if no previous transactions (shouldn't ever occur)
            if debug_mode:
                print('DEBUG: First transaction')   # DEBUG
            self.u += current_t.u                   # Add units to fund
            self.bc += current_t.v                  # Add cost of purchase
            self.f = current_t.f                    # Update fund name
        
        # Adds transaction to the list
        self.t.append(transaction)
    
    ''' SELL TRANSACTION SECTION '''
    def sell(self, transaction):
        current_t = transaction
        price = self.bc / self.u
        
        self.u -= current_t.u
        self.bc = self.u * price
        self.f = current_t.f
        
        if logging and self.k == logging_key:
            print('LOG: Fund Name = ' + self.f)
            print('LOG: Removed ' + str(current_t.u) + ' units from the S104 pool')
            print('LOG: Current Units = ' + str(self.u))
            print('LOG: Running Cost = £' + '{:.2f}'.format(self.bc))
            print('')
        
        if debug_mode:
            print('DEBUG: Units sold')
        self.t.append(transaction)
    
    def convert_in(self, transaction):
        current_t = transaction
        
    def convert_out(self, transaction):
        current_t = transaction
    
    def transfer_in(self, transaction):
        current_t = transaction
    
    def transfer_out(self, transaction):
        current_t = transaction
    
    def distribution(self, transaction):
        current_t = transaction
    
    def equalisation(self, transaction):
        current_t = transaction
    

class T_Pool:
    def __init__(self):
        self.a = [] # Same day trades
        self.b = [] # 30 day trades
        self.x = [] # 104 trades
        
class Transaction:
    def __init__(self, transaction):
        self.k = transaction[0] # Key
        self.d = transaction[1] # Date
        self.f = transaction[2] # Fund name
        self.t = transaction[3] # Type of transaction
        self.u = transaction[4] # Units
        self.p = transaction[5] # Price
        self.v = transaction[6] # Value
        
        self.matched = 0
        
        if self.v == None:
            self.v = self.u * self.p    # Value bought
    
    def debug(self):
        print('T DEBUG: ' + self.f + ' ' + self.t + ' ' + str(self.u) + ' MATCHED: ' + str(self.matched))
    
    # Function to check if matched off against other units in pool
    def check_matched(self):
        if self.u == self.matched:
            return True
        else:
            return False
    
    def compare(self, external_transaction):
        t = external_transaction
        delta_time = self.d - t.d
        delta_time = -delta_time
        
        if delta_time.days == 0:
            return 0
        elif delta_time.days > 0 and delta_time.days <= 30:
            return 30
        else:
            return 104
