# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:27:24 2020

@author: VDinesh.Kumar
"""

"""

Multivariate Liner Regression

"""

import pandas as pd
import numpy as np


def hypothesis(theta, X, n):
    h = np.ones((X.shape[0],1))
    theta = theta.reshape(1,n+1)
    for i in range(0,X.shape[0]):
        h[i] = float(np.matmul(theta, X[i]))
    h = h.reshape(X.shape[0])
    return h



def BGD(theta, alpha, num_iters, h, X, y, n):
    cost = np.ones(num_iters)
    for i in range(0,num_iters):
        theta[0] = theta[0] - (alpha/X.shape[0]) * sum(h - y)
        for j in range(1,n+1):
            theta[j] = theta[j] - (alpha/X.shape[0]) * sum((h-y) * X.transpose()[j])
            
        h = hypothesis(theta, X, n)
        cost[i] = (1/X.shape[0]) * 0.5 * sum(np.square(h - y))
    theta = theta.reshape(1,n+1)
    return theta, cost


def linear_regression(X, y, alpha, num_iters):
    n = X.shape[1]
    one_column = np.ones((X.shape[0],1))
    X = np.concatenate((one_column, X), axis = 1)
    # initializing the parameter vector...
    theta = np.zeros(n+1)
    # hypothesis calculation....
    h = hypothesis(theta, X, n)
    # returning the optimized parameters by Gradient Descent...
    theta, cost = BGD(theta,alpha,num_iters,h,X,y,n)
    return theta, cost



"""
data = pd.read_csv("C:/Users/VDinesh.Kumar/Desktop/Mamamiyaaaaaa/IISC/Project/" + "sample_data.csv")

label_column = ['Y']
feature_columns = list(set(list(data.columns)) - set(label_column))

X_train = data[feature_columns] #feature set

y_train = data['Y'] #label set


#mean = np.ones(X_train.shape[1])
#std = np.ones(X_train.shape[1])
        
# calling the principal function with learning_rate = 0.0001 and 
# num_iters = 300000
theta, cost = linear_regression(X_train, y_train,
                                               0.0001, 300000)

# Getting the predictions...
X_train = np.concatenate((np.ones((X_train.shape[0],1)), X_train)
                         ,axis = 1)


predictions = hypothesis(theta, X_train, X_train.shape[1] - 1)



print(data['Y'])
print("="*40)
print(theta)
print("="*40)
print(predictions)

"""