# Online Team-4 API 
#Author: Shikhar Jain & Aparna

import os
import sys
import enum
import numpy as np

class InputData(object):
    def __init__(self):
        self.sample_size = 0  # Number of samples. This is also the number of 'rows' in the nested list.
        self.indep_vars = 0   # Number of independent variables in the input.
        self.indep_vars_matrix = []
        self.dep_var_matrix = []

def performMatrixTranspose(input_matrix):
    M = np.array(input_matrix)
    #print(M)
    MTrans = np.transpose(M)
    #print(MTrans)
    return MTrans

def performMatrixInverse(input_matrix):
    import numpy as np
    M = np.array(input_matrix)
    #print(M)
    Minv = np.linalg.inv(M)
    #print(Minv)
    return Minv
    
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
    
    return result
    
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

def pedictHigherOrderRegression(input_x, coeff_matrix, regression, order):
    predict_data = InputData()
    predict_data.sample_size = 1
    predict_data.indep_vars = len(input_x)
    input_data = InputData()
    input_data.indep_vars_matrix = [input_x]
    input_data.indep_vars = len(input_x)
    input_data.sample_size = 1

    if regression == regression_type.polynomial:
        series_matrix =[]
        for i in range(1,input_data.indep_vars+1):
            series_matrix.append(0)
        predict_data.indep_vars = 0
        performPolynomialMatrixFormation(input_data, predict_data, series_matrix, 1, order)
        #print(data.indep_vars_matrix)
        #print(data.indep_vars, data.sample_size)
    else:
        predict_data.indep_vars = len(input_x)
        for x in input_data.indep_vars_matrix:
            x_arr = []
            x_arr.append(1)
            for xi in x:
                if regression == regression_type.logarithmic or regression == regression_type.power:
                    x_arr.append(np.log(xi))
                else:
                    x_arr.append(xi)
            predict_data.indep_vars_matrix.append(x_arr)
    
    i = 0
    cMatrix = coeff_matrix.copy()
    for coeff in cMatrix:
        if regression == regression_type.exponential:
            coeff[0] = np.log(coeff[0])
        elif regression == regression_type.power and i == 0:
            coeff[0] = np.log(coeff[0])
        i+=1

    i=0
    output = 0
    for seq in predict_data.indep_vars_matrix:
        output = 0
        j = 0
        for coeff in cMatrix:
            output += (coeff[0] * seq[j])
            j+=1
        if regression == regression_type.reciprocal:
            output = 1/output
        elif regression == regression_type.power or regression == regression_type.exponential:
            output = np.exp(output)
        output = round(output,2)
        i+=1

    return output
    
def performHigherOrderRegression(input_data, regression, order):
    #print("\nInput Independent parameters, X:\n", input_data.indep_vars_matrix)
    #print("\nInput Dependent parameters, Y:\n", input_data.dep_var_matrix)

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

    #print("\nPredicted values of Y:\n", output,"\n")

    i = 0
    for coeff in coeff_matrix:
        if regression == regression_type.exponential:
            coeff[0] = np.exp(coeff[0])
        elif regression == regression_type.power and i == 0:
            coeff[0] = np.exp(coeff[0])
        i+=1

    return output, coeff_matrix
    
