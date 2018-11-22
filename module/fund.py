from datetime import datetime, timedelta

class Fund:
    def __init__(self, key, date, fund_name, units, price, book_price, book_cost, value, gain):
        self.k = key
        self.d = date
        self.f = fund_name
        self.u = units
        self.p = price
        self.bp = book_price
        self.bc = book_cost
        self.v = value
        self.g = gain
        self.t = []
        self.converted = 0 # Value when converting
        
        if self.bc == None:
            self.bc = 0
        
        if self.bp = None:
            self.bp = 0
    
    def tran(self, transaction):
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
        
        for transactions in self.t:
            if t.compare(transaction) == 0:
                day_a.append(transaction)
            elif t.compare(transaction) == 30:
                day_b.append(transaction)
            else:
                day_x.append(transaction)
        
        
        
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
        elif delta_time.days > 0 and <= 30:
            return 30
        else:
            return 104
    
    