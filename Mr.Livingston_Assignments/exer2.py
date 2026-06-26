# 1.	Consider the tuple below;
# x = (“samsung”, “iphone”, “tecno”, “redmi”)
# 	Write a python program to output your favorite phone brand.
x = ("samsung", "iphone", "tecno", "redmi")
print("My favorite phone brand is:", x[0])

# 2.	Use negative indexing to print the 2nd last item in your tuple. 
print("The 2nd last item in the tuple is:", x[-2])

# 3.	Using the phones list above, write a python program to update “iphone” to “itel”
# Tuples are immutable, so we cannot update an item directly. However, we can convert the tuple to a list, update the item, and then convert it back to a tuple.
phones_list = list(x)
phones_list[1] = "itel"
x = tuple(phones_list)
print("The updated tuple is:", x)

# 4.	Write a python program to add “Huawei” to your tuple.
phones_list.append("Huawei")
x = tuple(phones_list)
print("The updated tuple is:", x)

# 5.	Write a python program to loop through the tuple above.
for phone in x:
    print(phone)

# 6.	Write a python program to remove/delete the first item in your tuple.
# Tuples are immutable, so we cannot remove an item directly. However, we can convert the tuple to a list, remove the item, and then convert it back to a tuple.
phones_list = list(x)
phones_list.pop(0)
x = tuple(phones_list)
print("The updated tuple is:", x)

# 7.	Using the tuple() constructor, create a tuple of the cities in Uganda.
cities = tuple(["Kampala", "Entebbe", "Jinja", "Mbarara"])
print("The tuple of cities in Uganda is:", cities)

# 8.	Write a python program to unpack your tuple.
city1, city2, city3, city4 = cities
print("The unpacked cities are:", city1, city2, city3, city4)

# 9.	Use a range of indexes to print the 2nd, 3rd and 4th cities in your tuple above.
print("The 2nd, 3rd and 4th cities are:", cities[1:4])

# 10.	Write two tuples, one containing your first names and the other your second names. Join the two tuples.
first_names = tuple(["John", "Jane", "Bob"])
second_names = tuple(["Doe", "Smith", "Johnson"])
full_names = first_names + second_names
print("The joined tuple is:", full_names)

# 11.	Create a tuple of colors and multiply it by 3.
colors = tuple(["red", "green", "blue"])
multiplied_colors = colors * 3
print("The multiplied tuple is:", multiplied_colors)

# 12.	Return the number of times 8 appears in this tuple
# thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
count_8 = thistuple.count(8)
print("The number of times 8 appears in the tuple is:", count_8)
