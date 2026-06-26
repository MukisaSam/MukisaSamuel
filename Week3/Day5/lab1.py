#9.1
class Restaurant:
    def __init__(self, name, cuisine_type):
        self.name = name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(f"{self.name} serves {self.cuisine_type} cuisine.")

    def open_restaurant(self):
        print(f"{self.name} is now open!")

restaurant1 = Restaurant("Pasta Palace", "Italian")
print(restaurant1.name)
print(restaurant1.cuisine_type)
restaurant1.describe_restaurant()
restaurant1.open_restaurant()

#9.2
restaurant2 = Restaurant("Sushi World", "Japanese")
restaurant3 = Restaurant("Taco Town", "Mexican")
restaurant4 = Restaurant("Burger Barn", "American")

restaurant2.describe_restaurant()
restaurant3.describe_restaurant()
restaurant4.describe_restaurant()

#9.3
class User:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def describe_user(self):
        print(f"User: {self.first_name} {self.last_name}, Email: {self.email}")

    def greet_user(self):
        print(f"Hello, {self.first_name}")

user1 = User("John", "Doe", "john.doe@example.com")
user2 = User("Jane", "Smith", "jane.smith@example.com")

user1.describe_user()
user1.greet_user()

user2.describe_user()
user2.greet_user()
