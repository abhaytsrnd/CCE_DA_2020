"""Linear Regression
APIs
1. fit
2. stats
3. params
4. predicts
5. predict
"""
import logging

from dataanalytics.stats_linear_regression.statistics import Statistics
from dataanalytics.stats_linear_regression.matrix import Matrix

class LinearRegression:

    def __init__(self):
        logging.debug('Initialized Linear Regression!!')
        self.__variables__: int = 0
        self.__params__: [float] = None
        self.__stats__ = [{}]

    def fit(self, data:[[float]], y:[float]) -> ([{}], [float], [float]):
        logging.info("log: Linear Regression Model Fit Invoked.")
        self.__validate(data, y)
        self.__stats__ = self.__stats(data, y)
        self.__variables__ = len(data)

        m1, m2 = self.__regression_matrix(data, y)
        m1_inverse = Matrix.inverse(m1)

        params = Matrix.multiply(m1_inverse, [m2])
        params = params[0]
        self.__params__ = params

        ycap = self.predicts(data)
        return (self.__stats__, self.__params__, ycap)

    def stats(self) -> []:
        return self.__stats__

    def params(self) -> []:
        return self.__params__

    def predicts(self, data:[[float]]) -> [float]:
        if(self.__variables__ != len(data)):
            raise ValueError('Number of Independent Variables Should be equal to ' + str(self.__variables__) + '!!')
        ycap = [0.0 for i in range(len(data[0]))]
        for i in range(len(data[0])):
            point = [0.0 for i in range(self.__variables__)]
            for j in range(self.__variables__):
                point[j] = data[j][i]
            yhat = self.predict(point)
            ycap[i] = yhat
        return ycap

    def predict(self, point:[float]) -> float:
        if(self.__variables__ != len(point)):
            raise ValueError('Number of Independent Variables Should be equal to ' + str(self.__variables__) + '!!')
        ycap = 0.0
        for i in range(self.__variables__):
            ycap = ycap + self.__params__[i]*point[i]
        ycap = ycap + self.__params__[self.__variables__]
        return ycap

    #########################
    #### Private Methods ####
    #########################

    def __regression_matrix(self, data:[[]], y:[]) -> ([[]], []):
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
                m1[j][k] = self.__multiply_and_sum(x, data[k])
            m1[j][variables] = sum(x)
            m2[j] = self.__multiply_and_sum(x, y)
        #b0
        for k in range(variables):
            m1[variables][k] = sum(data[k])
        m1[variables][variables] = len(y)
        m2[variables] = sum(y)
        return (m1, m2)

    def __multiply_and_sum(self, arr1: [], arr2: []) -> float:
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

    def __stats(self, data:[[float]], y:[float]) -> []:
        stats = [{} for i in range(len(data) + 1)]
        y_stats = Statistics.describe(y)
        (y_variance, y_std) = Statistics.variance(y, y_stats["mean"])
        y_stats["covariance"] = y_variance
        y_stats["r"] = 1.0
        for i in range(len(data)):
            s = Statistics.describe(data[i])
            (covariance, r) = Statistics.covariance(data[i], y, s["mean"], y_stats["mean"])
            s["covariance"] = covariance
            s["r"] = r
            stats[i] = s
        stats[len(data)] = y_stats
        return stats

    def __validate(self, data:[[float]], y:[float]):
        if data is None or len(data) == 0:
            raise ValueError("Data could not be None or Empty!!")
        elif y is None or len(y) == 0:
            raise ValueError("Y could not be None or Empty!!")
        n = len(y)
        for d in data:
            if len(d) != n:
                raise ValueError("No of Data Points should be eqaul to " + str(n) + " !!")
