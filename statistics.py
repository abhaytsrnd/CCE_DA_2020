"""Statistics
APIs
1. mean
2. variance
3. coVariance
4. correlation_coefficient
5. describe
6. yule_walker_eq
7. partial_correlation
8. correlation_matrix
9. partial_correlation_matrix
"""


import logging
import math
from matrix import Matrix

class Statistics:

    def __init__(self):
        logging.debug('Initialized Statistics!!')

    @staticmethod
    def mean(data: [float]) -> float:
        logging.debug("log: Calculate Mean Invoked.")
        Statistics.__validate(data)
        sum = 0.0
        for v in data:
            sum = sum + v
        mean = sum / len(data)
        return mean

    @staticmethod
    def variance(data: [float], mean: float = None) -> (float, float):
        logging.debug("log: Calculate Variance Invoked.")
        Statistics.__validate(data)
        if mean is None:
            mean = Statistics.mean(data)
        sum = 0.0
        for v in data:
            sum = sum + ((v - mean) * (v - mean))
        variance = sum / (len(data)-1)
        std = math.sqrt(variance)
        return (variance, std)

    @staticmethod
    def covariance(data_x: [float], data_y: [float], mean_x: float = None, mean_y: float = None) -> (float, float):
        logging.debug("log: Calculate CoVariance Invoked.")
        Statistics.__validate(data_x)
        Statistics.__validate(data_y)
        n_x = len(data_x)
        n_y = len(data_y)
        if(n_x != n_y):
            raise ValueError('Length of X & Y Should be equal!')
        if mean_x is None:
            mean_x = Statistics.mean(data_x)
        if mean_y is None:
            mean_y = Statistics.mean(data_y)
        n = n_x
        sum_cov = 0.0
        sum_var_x = 0.0
        sum_var_y = 0.0
        for i in range(n):
            sum_cov = sum_cov + ((data_x[i] - mean_x) * (data_y[i] - mean_y))
            sum_var_x = sum_var_x + ((data_x[i] - mean_x) * (data_x[i] - mean_x))
            sum_var_y = sum_var_y + ((data_y[i] - mean_y) * (data_y[i] - mean_y))
        cov = sum_cov / (n-1)
        variance_x = sum_var_x / (n-1)
        variance_y = sum_var_y / (n-1)
        r = Statistics.correlation_coefficient(cov, variance_x, variance_y)
        return (cov, r)

    @staticmethod
    def correlation_coefficient(cov: float, variance_x: float, variance_y: float) -> float:
        logging.debug("log: Calculate Correlation Coefficient Invoked.")
        r = cov / math.sqrt(variance_x * variance_y)
        return r

    @staticmethod
    def describe(data: [float]) -> {}:
        logging.debug("log: Describe Invoked.")
        Statistics.__validate(data)
        mean = Statistics.mean(data)
        (variance, std) = Statistics.variance(data, mean)
        stats = {}
        stats["count"] = len(data)
        stats["mean"] = mean
        stats["variance"] = variance
        stats["std"] = std
        stats["min"] = min(data)
        stats["max"] = max(data)
        return stats

    @staticmethod
    def __validate(data:[float]):
        if data is None or len(data) == 0:
            raise ValueError("Data could not be None or Empty!!")

    #############################
    #### Partial Correlation ####
    #############################

    #Yule - Walker Equations
    def yule_walker_eq(r12: float, r13: float, r23: float) -> float:
        if r12 is None or r13 is None or r23 is None:
            raise ValueError("Data could not be None or Empty!!")
        if r12 > 1 or r12 < -1 or r13 > 1 or r13 < -1 or r23 > 1 or r23 < -1:
            raise ValueError("Correlation Coefficient could not less than -1 and greater than 1!!" + "r12: " + str(r12) + " r13: " + str(r13) + " r23: " + str(r23))
        r12_3 = 0.0
        num = (r12 - (r13*r23))
        den = math.sqrt((1-(r13*r13)) * (1-(r23*r23)))
        r12_3 = num/den
        return r12_3

    @staticmethod
    def partial_correlation(data_y: [float], data_x:[float], eliminate:[[float]]) -> float:
        Statistics.__validate(data_y)
        Statistics.__validate(data_x)
        if len(data_y) != len(data_x):
            raise ValueError("Data Y & X should be of same dimension!!" + str(len(data_y)) + " != " + str(len(data_x)))
        Matrix.validate(eliminate)
        n = len(data_y)
        if n != len(eliminate[0]):
            raise ValueError("Data Y, X & Eliminate should be of same dimension!!" + str(n) + " != " + str(len(eliminate[0])))

        m = len(eliminate) + 2
        data = [[0.0 for x in range(n)] for x in range(m)]
        for i in range(m):
            if i == 0:
                data[i] = data_y
            elif i == 1:
                data[i] = data_x
            else:
                data[i] = eliminate[i-2]
        mat = Statistics.partial_correlation_matrix(data)
        return mat[0][1]

    @staticmethod
    def correlation_matrix(data: [[float]]) -> [[float]]:
        Matrix.validate(data)
        m = len(data)

        corr_m = [[None for x in range(m)] for x in range(m)]

        for j in range(m):
            for k in range(m):
                if corr_m[j][k] is None:
                    cov, r = Statistics.covariance(data[j], data[k])
                    corr_m[j][k] = r
                    corr_m[k][j] = r
        return corr_m

    @staticmethod
    def partial_correlation_matrix(data: [[float]]) -> [[float]]:
        m = len(data)
        corr_m = Statistics.correlation_matrix(data)
        corr_mi = Matrix.inverse(corr_m)

        par_corr_m = [[None for x in range(m)] for x in range(m)]

        for j in range(m):
            for k in range(m):
                if j == k:
                    par_corr_m[j][k] = 1.0
                else:
                    den =  -1 * math.sqrt(corr_mi[j][j] * corr_mi[k][k])
                    r = corr_mi[j][k] / den
                    par_corr_m[j][k] = r

        return par_corr_m
