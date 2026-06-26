# 1.	With reference to the dictionary below, write a python program to print the value of the shoe size. 
# Add this dictionary to your .py file
# Shoes = {
# 	“brand” : “Nick”,
# 	“color” : “black”,
# 	“size” : 40
# 	}
Shoes = {
    "brand": "Nick",
    "color": "black",
    "size": 40
}
print("The shoe size is:", Shoes["size"])   

# 2.	Write a python program to change the value “Nick” to “Adidas”
Shoes["brand"] = "Adidas"
print("The updated dictionary is:", Shoes)

# 3.	Write a python program to add a key/value pair "type”: "sneakers" to the dictionary
Shoes["type"] = "sneakers"
print("The updated dictionary is:", Shoes)

# 4.	Write a python program to return a list of all the keys in the dictionary above.
print("The keys in the dictionary are:", list(Shoes.keys()))

# 5.	Write a python program to return a list of all the values in the dictionary above.
print("The values in the dictionary are:", list(Shoes.values()))

# 6.	Check if the key “size” exists in the dictionary above.
if "size" in Shoes:
    print("The key 'size' exists in the dictionary.")
else:
    print("The key 'size' does not exist in the dictionary.")

# 7.	Write a python program to loop through the dictionary above.
for key, value in Shoes.items():
    print(f"{key}: {value}")

# 8.	Write a python program to remove “color” from the dictionary.
del Shoes["color"]
print("The updated dictionary is:", Shoes)

# 9.	Write a python program to empty the dictionary above.
Shoes.clear()
print("The updated dictionary is:", Shoes)

# 10.	Write a dictionary of your choice and make a copy of it.
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
copied_dict = my_dict.copy()
print("The original dictionary is:", my_dict)
print("The copied dictionary is:", copied_dict)

# 11.	Write a python program to show nested dictionaries
nested_dict = {
    "person1": {
        "name": "Alice",
        "age": 30
    },
    "person2": {
        "name": "Bob",
        "age": 25
    }
}
print("The nested dictionary is:", nested_dict)
