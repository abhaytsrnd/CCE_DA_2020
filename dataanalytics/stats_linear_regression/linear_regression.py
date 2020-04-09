"""Linear Regression
APIs
1. Regression
2.
"""
import logging

from dataanalytics.stats_linear_regression.statistics import Statistics
from dataanalytics.stats_linear_regression.matrix import Matrix

class LinearRegression:

    def __init__(self):
        logging.debug('Initialized LinearRegression!!')

    @staticmethod
    def model(data:[[]], y:[]) -> {}:
        logging.debug("log: Linear Regression Invoked.")
        m1, m2 = LinearRegression.__regression_matrix(data, y)
        m1_inverse = Matrix.inverse(m1)

        params = Matrix.multiply(m1_inverse, [m2])
        return params[0]

    #########################
    #### Private Methods ####
    #########################

    @staticmethod
    def __regression_matrix(data:[[]], y:[]) -> ([[]], []):
        logging.debug("log: Linear Regression Matrix Invoked.")
        variables = len(data)
        total_variables = len(data) + 1
        logging.debug("log: No of variables to be estimated = " + str(total_variables))
        m1 = [[0.0 for x in range(total_variables)] for x in range(total_variables)]
        m2 = [0.0 for x in range(total_variables)]
        #b1,b2,b3,...
        for j in range(variables):
            x = data[j]
            for k in range(variables):
                m1[j][k] = LinearRegression.__multiply_and_sum(x, data[k])
            m1[j][variables] = sum(x)
            m2[j] = LinearRegression.__multiply_and_sum(x, y)
        #b0
        for k in range(variables):
            m1[variables][k] = sum(data[k])
        m1[variables][variables] = len(y)
        m2[variables] = sum(y)
        return (m1, m2)

    @staticmethod
    def __multiply_and_sum(arr1: [], arr2: []) -> float:
        logging.debug("log: Calculate Multiply And Sum Invoked.")
        n1 = len(arr1)
        n2 = len(arr1)
        if(n1 != n2):
            raise ValueError('Length of Arr1 & Arr2 Should be equal!')
        n = n1
        sum = 0.0
        for i in range(n):
            sum = sum + (arr1[i] * arr2[i])
        return sum
