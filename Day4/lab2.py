#write a function that takes in input and calculates area of a rectangle

def area(length, width):
    return length * width
def input_var():
    a = float(input("Enter the length of the rectangle: "))
    b = float(input("Enter the width of the rectangle: "))
    return area(a, b)
input_var()