#By Mukisa Samuel, Reg No. 24/U/0752, Std No. 2400700752

#Bill Split Calculator

#Inputs and validation
total_bill_amount = float(input("Enter bill amount: "))
if total_bill_amount < 0:
    print("Bill amount cannot be negative.")
elif total_bill_amount == 0:
    print("Bill amount cannot be zero.")
    exit()

number_of_people = int(input("Enter number of people: "))
if number_of_people <= 0:
    print("Number of people must be a positive integer.")
    exit()

tip_percentage = float(input("Enter tip percentage: "))
if tip_percentage < 0:
    print("Tip percentage cannot be negative.")
elif tip_percentage > 100:
    print("Tip percentage cannot exceed 100%.")
elif tip_percentage == 0:
    print("Tip percentage cannot be zero.")
    exit()

#Calculate tip and total amounts
print("\nCalculating...\n")
tip_amount = (tip_percentage / 100) * total_bill_amount
total_amount = total_bill_amount + tip_amount
amount_per_person = total_amount / number_of_people

print("Receipt:")
print(f"Bill amount: ${total_bill_amount:.2f}")
print(f"Tip amount: ${tip_amount:.2f}")
print(f"Total amount: ${total_amount:.2f}")
print(f"Amount per person: ${amount_per_person:.2f}")