"""Linear Regression
APIs
1. fit
2. stats
3. model_stats
4. params
5. correlation_matrix
6. partial_correlation_matrix
7. predict
8. predicts
"""
import logging

from dataanalytics.stats_linear_regression.statistics import Statistics
from dataanalytics.stats_linear_regression.matrix import Matrix

class LinearRegression:

    def __init__(self):
        logging.debug('Initialized Linear Regression!!')
        self.__variables__: int = 0
        self.__corr_mat__ = [[float]]
        self.__partial_mat__ = [[float]]
        self.__stats__ = [{}]
        self.__model_stats__ = {}
        self.__params__: [float] = None
        self.__ycap__: [float] = None

    def fit(self, data:[[float]], y:[float]) -> ([{}], [float], [float]):
        logging.info("log: Linear Regression Model Fit Invoked.")
        self.__validate(data, y)
        self.__variables__ = len(data)

        merge_data = [[None for x in range(len(y))] for x in range(len(data)+1)]
        for i in range(len(merge_data)):
            if i == 0:
                merge_data[i] = y
            else:
                merge_data[i] = data[i-1]

        self.__corr_mat__ = Statistics.correlation_matrix(merge_data)
        self.__partial_mat__ = Statistics.partial_correlation_matrix(merge_data)
        self.__stats__ = self.__stats(data, y)

        m1, m2 = self.__regression_matrix(data, y)
        m1i = Matrix.inverse(m1)
        m1it = Matrix.transpose(m1i)
        m2t = Matrix.transpose([m2])

        params = Matrix.multiply(m1it, m2t)
        params = Matrix.transpose(params)
        params = params[0]
        self.__params__ = params

        self.__ycap__ = self.predicts(data)
        self.__model_stats__ = self.__model_stats(y, self.__ycap__)
        return (self.__stats__, self.__params__, self.__ycap__)

    def stats(self) -> [{}]:
        return self.__stats__

    def model_stats(self) -> {}:
        return self.__model_stats__

    def params(self) -> [float]:
        return self.__params__

    def ycap(self) -> [float]:
        return self.__ycap__

    def correlation_matrix(self) -> [[float]]:
        return self.__corr_mat__

    def partial_correlation_matrix(self) -> [[float]]:
        return self.__partial_mat__

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
        y_stats["pr"] = 1.0
        stats[0] = y_stats
        for i in range(len(data)):
            s = Statistics.describe(data[i])
            (covariance, r) = Statistics.covariance(data[i], y, s["mean"], y_stats["mean"])
            s["covariance"] = covariance
            s["r"] = r
            s["pr"] = self.__partial_mat__[0][i+1]
            stats[i+1] = s
        return stats

    def __model_stats(self, y:[float], ycap:[float]) -> {}:
        error = [0.0 for x in range(len(y))]
        for i in range(len(y)):
            error[i] = y[i] - ycap[i]
        s = Statistics.describe(error)
        return s

    def __validate(self, data:[[float]], y:[float]):
        if data is None or len(data) == 0:
            raise ValueError("Data could not be None or Empty!!")
        elif y is None or len(y) == 0:
            raise ValueError("Y could not be None or Empty!!")
        Matrix.validate(data)
        if len(data[0]) != len(y):
            raise ValueError("No of Data Points should be eqaul to " + str(len(y)) + " !!")
