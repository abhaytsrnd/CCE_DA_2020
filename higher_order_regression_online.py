#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import sys
import enum
import numpy as np


# In[10]:


class InputData(object):
    def __init__(self):
        self.sample_size = 0  # Number of samples. This is also the number of 'rows' in the nested list.
        self.indep_vars = 0   # Number of independent variables in the input.
        self.indep_vars_matrix = []
        self.dep_var_matrix = []

# In[12]:


def performMatrixTranspose(input_matrix):
    M = np.array(input_matrix)
    #print(M)
    MTrans = np.transpose(M)
    #print(MTrans)
    return MTrans


# In[13]:


def performMatrixInverse(input_matrix):
    import numpy as np
    M = np.array(input_matrix)
    #print(M)
    Minv = np.linalg.inv(M)
    #print(Minv)
    return Minv


# In[14]:


def performMatrixMultiply(matrix1, matrix2):
    # TODO: perform dimension check to see if matrices can be multiplied or not.
    
    #result = np.zeros((3,3))
    #print("Row Length of matrix1 is:", len(matrix1))
    #print("Column of matrix1 is:", len(matrix1[0]))
    #print("Row Length of matrix2 is:", len(matrix2))
    #print("Column of matrix2 is:", len(matrix2[0]))
    
    #If len(matrix1[0]) = len(matrix2):
    result = np.zeros((len(matrix1),len(matrix2[0])))
        
        # iterate through rows of matrix1
    for i in range (len(matrix1)):
        # iterate through columns of Y
        for j in range (len(matrix2[0])):
            # iterate through rows of Y
            for k in range (len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]                 
                
 
    #print (result)
        
        
    return result


# In[15]:


def performMultipleRegressionForLinearFit(data):
    X_Trans = performMatrixTranspose(data.indep_vars_matrix)
    #print(X_Trans)
    #print(data.indep_vars_matrix)
    
    X_Trans_X = performMatrixMultiply(X_Trans,data.indep_vars_matrix)
    #print(X_Trans_X)
    Dep_var_matrix = []
    for y in data.dep_var_matrix:
        Dep_var_matrix.append([y])
    X_Trans_Y = performMatrixMultiply(X_Trans,Dep_var_matrix)
    #print(X_Trans_Y)
    Inv_X_Trans_X = performMatrixInverse(X_Trans_X)
    #print(Inv_X_Trans_X)
    result_matrix = performMatrixMultiply(Inv_X_Trans_X,X_Trans_Y)
    #print("\n", result_matrix)
    return result_matrix
    


# In[16]:

reciprocal_input_data = InputData()
reciprocal_input_data.sample_size = 53
reciprocal_input_data.indep_vars = 3
reciprocal_input_data.indep_vars_matrix = [[5.94,5.31,0.29],
                          [6,5.6,-0.11],
                          [6.08,5.49,0.31],
                          [6.17,5.8,-0.19],
                          [6.14,5.61,-0.33],
                          [6.09,5.28,-0.09],
                          [5.87,5.19,-0.01],
                          [5.84,5.18,0.12],
                          [5.99,5.3,-0.07],
                          [6.12,5.23,0.41],
                          [6.42,5.64,-0.02],
                          [6.48,5.62,0.05],
                          [6.52,5.67,0.16],
                          [6.64,5.83,-0.3],
                          [6.75,5.53,0.23],
                          [6.73,5.76,0.33],
                          [6.89,6.09,0.43],
                          [6.98,6.52,0.16],
                          [6.98,6.68,0.39],
                          [7.1,7.07,0.05],
                          [7.19,7.12,0.13],
                          [7.29,7.25,0.6],
                          [7.65,7.85,0.17],
                          [7.75,8.02,-0.15],
                          [7.72,7.87,-0.73],
                          [7.67,7.14,0.06],
                          [7.66,7.2,0.39],
                          [7.89,7.59,0.15],
                          [8.14,7.74,-0.23],
                          [8.21,7.51,-0.05],
                          [8.05,7.46,-0.37],
                          [7.94,7.09,-0.27],
                          [7.88,6.82,-0.6],
                          [7.79,6.22,-0.61],
                          [7.41,5.61,-0.13],
                          [7.18,5.48,-0.7],
                          [7.15,4.78,-0.64],
                          [7.27,4.14,0.5],
                          [7.37,4.64,0.88],
                          [7.54,5.52,0.43],
                          [7.58,5.95,0.25],
                          [7.62,6.2,-0.17],
                          [7.58,6.03,-0.43],
                          [7.48,5.6,-0.34],
                          [7.35,5.26,-0.3],
                          [7.19,4.96,0.32],
                          [7.19,5.28,0.09],
                          [7.11,5.37,0.16],
                          [7.16,5.53,0.19],
                          [7.22,5.72,0.32],
                          [7.36,6.04,-0.38],
                          [7.34,5.66,0.09],
                          [7.3,5.75,0.07]
                          ]
    
reciprocal_input_data.dep_var_matrix = [1.146,-2.443,1.497,-0.132,2.025,0.737,-1.023,-0.956,0.385,0.983,5.092,3.649,2.703,-0.271,2.055,-0.714,
                       0.653,-0.034,-1.058,-2.051,1.451,-0.989,1.358,0.746,1.855,-1.894,0.781,-0.161,2.233,2.425,2.169,
                       0.982,4.708,6.063,9.382,9.304,10.690,6.531,7.873,3.882,4.960,1.301,1.154,0.116,4.928,2.530,8.425,
                       5.291,5.192,0.257,4.402,3.173,5.104,]

linear_input_data = InputData()
linear_input_data.sample_size = 5
linear_input_data.indep_vars = 2
linear_input_data.indep_vars_matrix = [[12,32],
                          [14, 35],
                          [15, 45],
                          [16, 50],
                          [18, 65]
                          ]
    
linear_input_data.dep_var_matrix = [350, 400, 430, 435, 433]

"Input data for logarithmic: https://courses.lumenlearning.com/ivytech-collegealgebra/chapter/build-a-logarithmic-model-from-data/"
log_input_data = InputData()
log_input_data.sample_size = 12
log_input_data.indep_vars = 1
log_input_data.indep_vars_matrix = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12]]
    
log_input_data.dep_var_matrix = [47.3,50.0,54.1,59.7,62.9,68.2,69.7,70.8,73.7,75.4,76.8,78.7]

"Input data for power: http://www.real-statistics.com/regression/power-regression/"
power_input_data = InputData()
power_input_data.sample_size = 11
power_input_data.indep_vars = 1
power_input_data.indep_vars_matrix = [[8.1],[69.9],[4.2],[14.1],[5.6],[52.1],[44.6],[19.6],[33],[6.7],[30.1]]
    
power_input_data.dep_var_matrix = [33,49,19,27,23,51,34,32,28,36,43]

"Input data for exponential: http://www.real-statistics.com/regression/exponential-regression-models/exponential-regression/"
exponential_input_data = InputData()
exponential_input_data.sample_size = 11
exponential_input_data.indep_vars = 1
exponential_input_data.indep_vars_matrix = [[45],[99],[31],[57],[37],[85],[21],[64],[17],[41],[103]]
    
exponential_input_data.dep_var_matrix = [33,72,19,27,23,62,24,32,18,36,76]

"Input data for polynomial: https://mathbits.com/MathBits/TISection/Statistics2/quadratic.html"
quadratic_input_data = InputData()
quadratic_input_data.sample_size = 13
quadratic_input_data.indep_vars = 1
quadratic_input_data.indep_vars_matrix = [[10],[15],[20],[24],[30],[34],[40],[45],[48],[50],[58],[60],[64]]
    
quadratic_input_data.dep_var_matrix = [115.6,157.2,189.2,220.8,253.8,269.2,284.8,285.0,277.4,269.2,244.2,231.4,180.4]

class regression_type(enum.Enum):
    linear = 1
    polynomial = 2
    reciprocal = 3
    logarithmic = 4
    exponential = 5
    power = 6

def performPolynomialMatrixFormation(input_data, data, series_matrix, index, order):
    prev_powers = 0
    for i in range(0,index-1):
        prev_powers += series_matrix[i]

    remaning_powers = order - prev_powers

    for i in range(0, remaning_powers+1):
        series_matrix[index - 1] = i
        if index < input_data.indep_vars:
            performPolynomialMatrixFormation(input_data, data, series_matrix, index+1, order)
        else:
            data.indep_vars +=1
            k =0
            for seq in input_data.indep_vars_matrix:
                j =0
                value = 1
                for series in series_matrix:
                    value *= seq[j]**series
                    j+=1
                if len(data.indep_vars_matrix) < (k+1):
                    data.indep_vars_matrix.append([value])
                else:
                    data.indep_vars_matrix[k].append(value)
                k+=1

def performMultipleRegression(input_data, regression, order):
    print("\nInput Independent parameters, X:\n", input_data.indep_vars_matrix)
    print("\nInput Dependent parameters, Y:\n", input_data.dep_var_matrix)

    data = InputData()
    data.sample_size = len(input_data.indep_vars_matrix)
    #print("Sample Size: ", data.sample_size, " Independent variables: ", data.indep_vars)
    for y in input_data.dep_var_matrix:
        if regression == regression_type.reciprocal:
            data.dep_var_matrix.append(1/y)
        elif regression == regression_type.power or regression == regression_type.exponential:
            data.dep_var_matrix.append(np.log(y))
        else:
            data.dep_var_matrix.append(y)

    #print(data.dep_var_matrix)
    if regression == regression_type.polynomial:
        series_matrix =[]
        for i in range(1,input_data.indep_vars+1):
            series_matrix.append(0)
        data.indep_vars = 0
        performPolynomialMatrixFormation(input_data, data, series_matrix, 1, order)
        #print(data.indep_vars_matrix)
        #print(data.indep_vars, data.sample_size)
    else:
        data.indep_vars = len(input_data.indep_vars_matrix[0])
        for x in input_data.indep_vars_matrix:
            x_arr = []
            x_arr.append(1)
            for xi in x:
                if regression == regression_type.logarithmic or regression == regression_type.power:
                    x_arr.append(np.log(xi))
                else:
                    x_arr.append(xi)
            data.indep_vars_matrix.append(x_arr)

    coeff_matrix = performMultipleRegressionForLinearFit(data)
    #print("\nCoefficient Matrix initial:\n",coeff_matrix)

    output =[]
    i=0
    for seq in data.indep_vars_matrix:
        output.append(0)
        j = 0
        for coeff in coeff_matrix:
            output[i] += (coeff[0] * seq[j])
            j+=1
        if regression == regression_type.reciprocal:
            output[i] = 1/output[i]
        elif regression == regression_type.power or regression == regression_type.exponential:
            output[i] = np.exp(output[i])
        output[i] = round(output[i],2)
        i+=1

    print("\nPredicted values of Y:\n", output,"\n")

    i = 0
    for coeff in coeff_matrix:
        if regression == regression_type.exponential:
            coeff[0] = np.exp(coeff[0])
        elif regression == regression_type.power and i == 0:
            coeff[0] = np.exp(coeff[0])
        i+=1
    print("\nCoefficient Matrix final:\n",coeff_matrix)

    


n = len(sys.argv)
order = 1
reg_type = "polynomial"
if n > 1:
    reg_type = sys.argv[1]

if n > 2:
    order = int(sys.argv[2])

if reg_type == "polynomial":
    performMultipleRegression(quadratic_input_data, regression_type.polynomial, order)
elif reg_type == "logarithmic":
    performMultipleRegression(log_input_data, regression_type.logarithmic, 0)
elif reg_type == "reciprocal":
    performMultipleRegression(reciprocal_input_data, regression_type.reciprocal, 0)
elif reg_type == "power":
    performMultipleRegression(power_input_data, regression_type.power, 0)
elif reg_type == "exponential":
    performMultipleRegression(exponential_input_data, regression_type.exponential, 0)
elif reg_type == "linear":
    performMultipleRegression(linear_input_data, regression_type.linear, 0)
else:
    print("\nUsage: python Multiple_Regression_transformation_v1.py <regression_type> <order>")
    print("\nRequired:\n", "<regression_type>: polynomial | logarithmic | reciprocal | power | exponential | linear")
    print("\nOptional:\n", "<order>: Number > 0")
