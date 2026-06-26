#how importing modules, standard python libraries 

# import sys as a
# print(a.builtin_module_names)

# import lab2 as b
# print(b.calc(5, 3))

# import lib1.calc as a
# print(a.add_no(5, 3))

# #short way to import a module from a different folder
from lib1 import calc
print(calc.add_no(5, 3))
