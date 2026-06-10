#PII
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
birth_year = input("Enter your birth year: ")
city = input("Enter your city of residence: ")
current_year = 2026
age = current_year - int(birth_year)

print(f"I am {first_name} {last_name}.\nI am {age} years old \t born \"{birth_year}\" \nI live in {city}.")