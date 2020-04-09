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
        logging.debug('Initialized Linear Regression!!')
        self._variables: int = 0
        self._params: [float] = None
        self._stats = []

    def stats(self) -> []:
        return self._stats

    def fit(self, data:[[float]], y:[float]) -> ():
        logging.info("log: Linear Regression Model Fit Invoked.")
        self._stats = self.__stats(data, y)
        self._variables = len(data)

        m1, m2 = self.__regression_matrix(data, y)
        m1_inverse = Matrix.inverse(m1)

        params = Matrix.multiply(m1_inverse, [m2])
        params = params[0]
        self._params = params

        ycap = self.predicts(data)
        return (self._stats, self._params, ycap)

    def predicts(self, data:[[float]]) -> [float]:
        if(self._variables != len(data)):
            raise ValueError('Number of Independent Variables Should be equal to ' + str(self._variables) + '!!')
        ycap = [0.0 for i in range(len(data[0]))]
        for i in range(len(data[0])):
            point = [0.0 for i in range(self._variables)]
            for j in range(self._variables):
                point[j] = data[j][i]
            yhat = self.predict(point)
            ycap[i] = yhat
        return ycap

    def predict(self, point:[float]) -> float:
        if(self._variables != len(point)):
            raise ValueError('Number of Independent Variables Should be equal to ' + str(self._variables) + '!!')
        ycap = 0.0
        for i in range(self._variables):
            ycap = ycap + self._params[i]*point[i]
        ycap = ycap + self._params[self._variables]
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
        y_stats["r"] = 1
        for i in range(len(data)):
            s = Statistics.describe(data[i])
            (covariance, r) = Statistics.covariance(data[i], y, s["mean"], y_stats["mean"])
            s["covariance"] = covariance
            s["r"] = r
            stats[i] = s
        stats[len(data)] = y_stats
        return stats
