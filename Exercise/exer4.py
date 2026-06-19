# 1.	Declare two variables, an integer and a string and use the correct method to concatenate the two variables.
integer_var = 5
string_var = "Hello"
concatenated_var = str(integer_var) + string_var
print("The concatenated variable is:", concatenated_var)

# 2.	Consider the example below;
# txt = “      Hello,       Uganda!       ”
# Output the string without spaces at the beginning, in the middle and at the end.
txt = "      Hello,       Uganda!       "
print("The string without spaces is:", txt.strip())

# 3.	Write a python program to convert the value of ‘txt’ to uppercase.
print("The string in uppercase is:", txt.upper())

# 4.	Write a python program to replace character ‘U’ with ‘V’ in the string above.
print("The string with 'U' replaced with 'V' is:", txt.replace('U', 'V'))   

# 5.	Using the code below, write a python program to return a range of characters in the 2nd, 3rd and 4th position.
# y = “I am proudly Ugandan”
y = "I am proudly Ugandan"
print("The characters in the 2nd, 3rd and 4th position are:", y[1:4])

# 6.	The piece of code below will give an error when output;
# x = “All “Data Scientists” are cool!” 
# Write a python program to correct it.
x = 'All "Data Scientists" are cool!'
print("The corrected string is:", x)
#or
x = "All \"Data Scientists\" are cool!"
print("The corrected string is:", x)
