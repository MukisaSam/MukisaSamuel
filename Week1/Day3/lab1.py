# a=5
# b=5
# c=5

# print(bool(a<b or b<c))
# print(bool(a<b and b<c))
# print(bool(a==b and b==c))
# print(bool(a is b))

# import keyword
# # print(keyword.kwlist)

# as = 2

# num1 = {"age": 10, "name": "Alice"}

# for ke, value in num1.items():
#     print(ke, value)

num2 = {
    "Person1": {"age": 10, "name": "Alice"},
    "Person2": {"age": 20, "name": "Bob"},
}
for key1, value1 in num2.items():
    for key2, value2 in value1.items():
        print(key2, value2)