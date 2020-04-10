"""Statistics
APIs
1. mean
2. variance
3. coVariance
4. correlation_coefficient
5. describe
"""
import logging
import math

class Statistics:

    def __init__(self):
        logging.debug('Initialized Statistics!!')

    @staticmethod
    def mean(data: [float]) -> float:
        logging.debug("log: Calculate Mean Invoked.")
        sum = 0.0
        for v in data:
            sum = sum + v
        mean = sum / len(data)
        return mean

    @staticmethod
    def variance(data: [float], mean: float = None) -> (float, float):
        logging.debug("log: Calculate Variance Invoked.")
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
