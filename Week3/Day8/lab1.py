class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
    
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Student ID: {self.student_id}")

s1 = Student("Alice", 20, "S12345")
s1.display_info()