#Contact management
from unicodedata import name


#phone checker
def check_phone(phone):
    if phone.isdigit() or (phone.startswith("+") and phone[1:].isdigit()):
        if len(phone) == 10 and phone.startswith("0"):
            return True
        elif len(phone) == 13 and phone.startswith("+256"):
            return True
        else:
            return False
    
def add_contact():
    name = input("Enter contact name: ")
    phone = input("Enter contact phone number: ")
    while not check_phone(phone):
        print("Invalid phone number. Please enter a valid phone number.")
        phone = input("Enter contact phone number: ")
    return name, phone

def print_contact(name, phone):
    print(f"\nContact Details:")
    print(f"Contact Name: {name}")
    print(f"Contact Phone Number: {phone}")

name, phone = add_contact()
print_contact(name, phone)