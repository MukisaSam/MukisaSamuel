# 1.	Create a list with 5 items (names of people) and write a python program to output the 2nd item.
names = ["Alice", "Bob", "Charlie", "David", "Eve"]
print("The second item in the list is:", names[1])

# 2.	Write a python program to change the value of the first item to a new value
names[0] = "Anna"
print("The updated list is:", names)

# 3.	Write a python program to add a sixth item to the list
names.append("Frank")
print("The updated list is:", names)

# 4.	Write a python program to add “Bathel” as the 3rd item in your list
names.insert(2, "Bathel")
print("The updated list is:", names)

# 5.	Write a python program to remove the 4th item from the list
names.pop(3)
print("The updated list is:", names)

# 6.	Use negative indexing to print the last item in your list
print("The last item in the list is:", names[-1])

# 7.	Create a new list with 7 items and use a range of indexes to print the 3rd, 4th and 5th items.
new_list = ["A", "B", "C", "D", "E", "F", "G"]
print("The 3rd, 4th and 5th items in the new list are:", new_list[2:5])

# 8.	Write a list of countries and make a copy of it.
countries = ["USA", "Canada", "UK", "Australia"]
countries_copy = countries.copy()
print("The copy of the countries list is:", countries_copy)

# 9.	Write a python program to loop through the list of countries
for country in countries:
    print(country)

# 10.	Write a list of animal names and sort them in both descending and ascending order.
animals = ["Lion", "Tiger", "Elephant", "Giraffe", "Zebra"]
animals.sort()
print("The sorted list of animals in ascending order is:", animals)
animals.sort(reverse=True)
print("The sorted list of animals in descending order is:", animals)

# 11.	Using the list above, write a python program to output only animal names with the letter ‘a’ in them
for animal in animals:
    if 'a' in animal:
        print(animal)

# 12.	Write two lists, one containing your first names and the other your second names. Join the two lists.
first_names = ["Alice", "Bob", "Charlie"]
second_names = ["Smith", "Johnson", "Williams"]
full_names = first_names + second_names
print("The joined list of full names is:", full_names)
