# Lab 1 Exercise 1: Create a method overloading and overriding the completes a banking system
# The parent class must be Transaction and the child class can be deposit, withdrwal and Transfer.
# Demonstrate an employer dpositing, witdrawing and transfering funds.
 
class Transaction:
    def __init__(self, amount):
        self.amount = amount

    def process(self):
        print(f"Processing transaction of amount: {self.amount}")

class Deposit(Transaction):
    def __init__(self, amount):
        super().__init__(amount)
    def process(self):
        print(f"Depositing amount: {self.amount}")
        self.amount += self.amount

class Withdrawal(Transaction):
    def __init__(self, amount):
        super().__init__(amount)
    def process(self):
        print(f"Withdrawing amount: {self.amount}")
        self.amount -= self.amount

class Transfer(Transaction):
    def __init__(self, amount, to_account):
        super().__init__(amount)
        self.to_account = to_account

    def process(self):
        print(f"Transferring amount: {self.amount} to account: {self.to_account}")

# Demonstration of the banking system
deposit = Deposit(2000)
withdrawal = Withdrawal(500)
transfer = Transfer(1000, 2)

deposit.process()
withdrawal.process()
transfer.process()