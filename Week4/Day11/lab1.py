import matplotlib.pyplot as plt
# x = [1, 2, 3, 4, 5]
# y = [2, 3, 5, 7, 11]
# z = [1, 4, 9, 16, 25]
# categories = ['A', 'B', 'C', 'D']
# values = [10, 20, 15, 25]

# fig, ax = plt.subplots()
# ax.plot (x, y, label='Data Points', color='blue', marker='o')
# ax.plot (x, z, label='Squared Values', color='red', marker='s')
# ax.bar(categories, values, color='green')
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_title('Simple Plot')
# ax.legend()
# plt.show()

# #bar graph
# categories = ['A', 'B', 'C', 'D']
# values = [10, 20, 15, 25]

# fig, ax = plt.subplots()
# ax.bar(categories, values, color='green')
# ax.set_xlabel('Categories')
# ax.set_ylabel('Values')
# ax.set_title('Bar Graph')
# plt.show()

# #Histogram
# data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
# fig, ax = plt.subplots()
# ax.hist(data, bins=8, color='blue', edgecolor='black')
# ax.set_xlabel('Value')
# ax.set_ylabel('Frequency')
# ax.set_title('Histogram')
# plt.show()

# #Scatter Plot
# x = [1, 2, 3, 4, 5]
# y = [2, 3, 5, 7, 11]
# fig, ax = plt.subplots()
# ax.scatter(x, y, color='red', marker='o')
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_title('Scatter Plot')
# plt.show()

#Heatmap
import matplotlib.pyplot as plt
import seaborn as sns
x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
sns.heatmap(x, annot=False, cmap='coolwarm')
plt.show()