# file = open("student.txt", "r")
# content = file.read()
# print(content)
# file.close()

# with open("student.txt", "r") as file:
#     content = file.read()
#     print(content)

#Exercise 1: Write a file with content "I love python programming" on the first line,
# "I am a becoming a data scientist" on the second line, save the file as report.txt

# with open("report.txt", "w") as file:
#     file.write("I love python programming\n")
#     file.write("I am becoming a data scientist\n")

#using report.txt, append "Every data scientist must learn python"
# with open("report.txt", "a") as file:
#     file.write("Every data scientist must learn python\n")

# import csv

# with open("students.csv", "a") as file:
#     writer = csv.writer(file)
#     writer.writerow(["2026/BSSE/006", "Mukisa Samuel", "Male", "22", "Software Engineering", "90"])

# with open("students.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(row)

import json

# Exercise 2: Write a JSON file with the following content:
# {
#     "name": "Mukisa Samuel",
#     "age": 22,
#     "course": "Software Engineering"
# }

# data = {
#     "name": "Mukisa Samuel",
#     "age": 22,
#     "course": "Software Engineering"
# }

# with open("student.json", "w") as file:
#     json.dump(data, file, indent=4)

# # Read the JSON file
# with open("student.json", "r") as file:
#     data = json.load(file)
#     print(data)

# Exercise 3: Write a custome exeception for a Ugandan to Drive a car, "Must be 18 years or older"
class UgandanCannotDriveException(Exception):
    def __init__(self, message="Must be 18 years or older"):
        self.message = message
        super().__init__(self.message)
    
age = int(input("Enter your age: "))
if age < 18:
    raise UgandanCannotDriveException
   