# class Car:
#     def __init__(self, brand, model, price):
#         self.brand = brand
#         self._model = model
#         self.__price = price

#     def display_info(self):
#         print(f"{self.brand} {self._model} ${self.__price:,.2f}")

# car1 = Car("Toyota", "Camry", 24000)
# car1.display_info()
# car2 = Car("Honda", "Civic", 22000)
# car2.display_info()

class MobileMoney:
    def __init__(self, balance):
        self.__balance = balance

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds.")
        else:
            self.__balance -= amount
    def deposit(self, amount):
        self.__balance += amount

    def check_balance(self):
        print(f"Balance: ${self.__balance:,.2f}")

account = MobileMoney(1000)
account.check_balance()
account.withdraw(200)
account.check_balance()
# print(account.__balance)

#what is abstraction
