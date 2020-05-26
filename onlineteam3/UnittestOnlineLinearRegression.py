import sys
import os

print (os.getcwd())

#print (os.path.abspath(__file__))

#sys.path.insert(0, os.getcwd())

sys.path.append(os.getcwd())

from Team3onlineLinearRegression import Team3onlineLinearRegression
 

x = [1,2,3,4,5,6,7,8,9,10]
y1 = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]
data = [x]
model = Team3onlineLinearRegression(data, y1)
params, stats, y_predicts = model.fit()

print("\nUNIT TEST 1\n")
print("x:",x)
print("y:",y1)
print ("Params",params)
print ("Stats",stats)
print ("y_predicts",y_predicts)

print("\nUNIT TEST 2\n")
print ("Mileage and Price Data")
mileage = [18, 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 24, 24, 25, 25, 25, 26, 26, 27, 27, 28, 30, 32, 33, 33, 33, 34, 35]
price = [14525, 13995, 15395, 12267, 12164, 14944, 14799, 11545, 24760, 17257, 14929, 13949, 17879, 11650, 13150, 23300, 13150, 14495, 12495, 16342, 15350, 13195, 17899, 10565, 9955, 14980, 21498, 16145, 13249, 9483, 9599, 10945, 10989, 10855, 10320, 9745, 13945, 13071, 11470, 6599, 8895, 7402, 9410, 5866, 6488]
data_1 = [mileage]


model = Team3onlineLinearRegression(data_1, price)
params, stats, y_predicts = model.fit()

print ("Params",params)
print ("Stats",stats)
print ("y_predicts",y_predicts)


print("\nUNIT TEST 3\n")
print ("Multiple Regression::: ")
X1 = [57, 59, 49, 62, 51, 50, 55, 48, 52, 42, 61, 57]
X2 = [8, 10, 6, 11, 8, 7, 10, 9, 10, 6, 12, 9]
Y = [64, 71, 53, 67, 55, 58, 77, 57, 56, 51, 76, 68]
data_2 = []
data_2.append(X1)
data_2.append(X2)

model = Team3onlineLinearRegression(data_2, Y)
params, stats, y_predicts = model.fit()

print ("Params",params)
print ("Stats",stats)
print ("y_predicts",y_predicts)
print("\n")
