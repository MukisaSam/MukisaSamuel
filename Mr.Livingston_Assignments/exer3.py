# 1.	Use the set() constructor to create a set of 3 of your favorite beverages.
beverages = set(["coffee", "tea", "juice"])

# 2.	Use the correct method to add 2 more items to the beverages set.
beverages.add("soda")
beverages.add("water")
print("The updated set of beverages is:", beverages)

# 3.	Given the set below;
# mySet = {“oven”, “kettle”, “microwave”, “refrigerator”}
# Check if microwave is present in the set.
mySet = {"oven", "kettle", "microwave", "refrigerator"}
if "microwave" in mySet:
    print("Microwave is present in the set.")
else:
    print("Microwave is not present in the set.")

# 4.	Write a python program to remove “kettle” from the set above.
mySet.remove("kettle")
print("The updated set is:", mySet)

# 5.	Write a python program to loop through the set above.
for item in mySet:
    print(item)

# 6.	Write a set of 4 items and a list of two items. Write a python program to add elements in the list to elements in the set.
items_set = {"apple", "banana", "cherry", "date"}
items_list = ["elderberry", "fig"]
items_set.update(items_list)
print("The updated set is:", items_set)

# 7.	Write two sets, one containing your ages and the other your first names. Join the two sets.
ages = {25, 30, 35}
first_names = {"Alice", "Bob", "Charlie"}
full_names = ages.union(first_names)
print("The joined set is:", full_names)
