import numpy as np

array1 = np.array([[1, 2, 3], [4, 5, 6]])
# print(array1[0,1])

#subtracting 1 from each element of the array
# array2 = array1 - 1
# print(array2)
array1[0,1] -= 1
print(array1)