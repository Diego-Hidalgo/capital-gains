
import json

class Operation :

    def __init__(self, a, p, q):
        self.action = a         #type of stock operation buy/sell
        self.price = p          #price of the buy/sell stock operation
        self.quantity = q       #quantity of stocks boughts/solds
    
    def calcTotal(self):
        return self.price * self.quantity

    def get_info(self):
        return f"action: {self.action} | price: ${self.price} | quantity: {self.quantity}"

class Auxiliar :

    MAX_TOTAL_AMOUNT = 20000   #the max amount allowed of sell (quantity * price) that does not pay taxes
    TAX_RATE = 0.2             #the rate in taxes to pay for a profit

    def __init__(self):
        self.prices = []        #list for the prices of the bought stocks
        self.quantities = []    #list for the quantities of the bought stocks
        self.total = 0          #total profit/loss
        self.avg_price = 0.0    #the weighted average price used to determine a profit/loss
        self.count = 0          #counter for the prices and quantities

    def calc_avg_price(self):
        num = 0.0
        for i in range(0, self.count):
            num += self.prices[i] * self.quantities[i]
        den = sum(self.quantities)
        self.avg_price = float((num / den))

    def taxes_to_pay(self, action, price, quantity):
        if (action == "buy"):
            return 0
            
        if (price < self.avg_price):
            self.total -= (self.avg_price - price) * quantity
            return 0
        else:
            self.total += (price - self.avg_price) * quantity

        if (price * quantity <= self.MAX_TOTAL_AMOUNT):
            return 0

        if (self.total > 0):
            tax = self.TAX_RATE * self.total
            self.total = 0
            return tax
        
        return 0

print("Hello World!")

operations = []                 #list of the registered operations
taxes = []                      #list of the taxes to pay

#read from the json file on the given path
@staticmethod
def read_from_json():
    case_path = input("\npath: ")
    print()
    with open(case_path) as file:
        data = json.load(file)
        for d in data:
            print(d)
            a = (d['operation'])
            p = (d['unit-cost'])
            q = (d['quantity'])
            operations.append(Operation(a, p, q))

#read the entries from the stdin
@staticmethod
def read_from_console():

    print("\nEntry format:")
    print("operation unit-cost quantity")
    print("to stop type -1\n")

    case = input()

    while(case != "-1"):
        parts = case.split(" ")
        operations.append(Operation(parts[0], float(parts[1]), float(parts[2])))
        case = input()

if (input("\nchoose entry method\n1-json \n2-console\n:") == "1"):
    read_from_json()
else:
    read_from_console()

aux = Auxiliar()

for op in operations:

    if (op.action == "buy"):
        aux.prices.append(op.price)
        aux.quantities.append(op.quantity)
        aux.count += 1
        aux.calc_avg_price()
        taxes.append(0)
        continue

    taxes.append(aux.taxes_to_pay(op.action, op.price, op.quantity))

print()

for tax in taxes :
    print(f'tax: {tax}')