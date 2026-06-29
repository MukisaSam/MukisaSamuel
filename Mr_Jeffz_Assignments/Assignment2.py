#By Mukisa Samuel, 24/U/0752, 2400700752

discount_coupon_code = [123, 456, 789]
location = ["Kampala", "Entebbe", "Jinja", "Gulu", "Mbarara"]

users = [
    {"name": "samuel", "password": "samuel123", "role": "Admin"},
    {"name": "bob", "password": "bob123", "role": "Cashier"},
    {"name": "eve", "password": "eve123", "role": "Customer"}
]

def login():
    tries = 3
    count = 0
    while count < tries:
        count += 1
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for user in users:
            if user["name"] == username and user["password"] == password:
                print(f"Login successful. Welcome, {username}! Your role is {user['role']}.")
                return user["role"]
        print(f"Invalid username or password. Please try again, {tries - count} tries remaining.")
    print("Too many failed login attempts. Access denied.")
    exit()
    return None

#inputs
role = login()
if role == "Cashier" or role == "Customer":
    subtotal = float(input("Enter the subtotal: "))
    coupon_code = int(input("Enter the discount coupon code: "))
    customer_location = input("Enter your location: ").strip().title()
    while customer_location not in location:
        print("Enter correct location")
        customer_location = input("Enter your location: ").strip().title()
elif role == "Admin":
    for user in users:
        print(f"Name: {user['name']}, Role: {user['role']}")
    print(f"Coupons: {', '.join([str(coupon) for coupon in discount_coupon_code])}")
    print(f"Tax rates by location: {list(zip(location, [10, 12, 8, 15, 11]))}")
    exit()

#calculations

# Using nested conditions to check if the coupon code is valid 
# and to calculate the discount amount based on subtotal
if coupon_code in discount_coupon_code:
    print("Valid coupon code. Applying discount.")
    if subtotal < 10000:
        coupon_discount_percent = 10
    elif subtotal >= 10000 and subtotal < 50000:
        coupon_discount_percent = 15
    elif subtotal >= 50000:
        coupon_discount_percent = 20
else:
    coupon_discount_percent = 0
    print("Invalid coupon code. No discount applied.")

# Using switch to check if the location is valid 
# and to calculate the tax based on the location
match customer_location:
    case "Kampala":
        tax_percent = 10
    case "Entebbe":
        tax_percent = 12
    case "Jinja":
        tax_percent = 8
    case "Gulu":
        tax_percent = 15
    case "Mbarara":
        tax_percent = 11

discount_amount = subtotal * (coupon_discount_percent / 100)
total_after_discount = subtotal - discount_amount
tax_amount = total_after_discount * (tax_percent / 100)
final_total = total_after_discount + tax_amount

#output per role
if role == "Cashier":
    print(f"Final Total: {final_total}")
elif role == "Customer":
    print(f"My Receipt:")
    print(f"Subtotal: {subtotal}")
    print(f"Discount Amount: {discount_amount}")
    print(f"Tax Amount: {tax_amount}")
    print(f"Final Total: {final_total}")
