"""Matrix
APIs
1. inverse
2. multiply
3.
"""
import logging
import math
import numpy as np


class Matrix:

    def __init__(self):
        logging.debug('Initialized Matrix!!')

    #TODO: Calculate Inverse without numpy
    @staticmethod
    def inverse(m: [[]]):
        logging.debug("log: Matrix inverse Invoked.")
        npm = np.array(m)
        npm_inverse = np.linalg.inv(npm)
        m_inverse = np.asarray(npm_inverse)
        return m_inverse

    #TODO: Make function more robust & generic
    @staticmethod
    def multiply(m1: [[]], m2:[[]]) -> []:
        logging.debug("log: Matrix multiply Invoked.")
        n = len(m1)
        m = 1
        mat = [[0.0 for x in range(n)] for x in range(m)]
        for j in range (n):
            for k in range (n):
                mat[0][j] = mat[0][j] + (m1[j][k] * m2[0][k])
        return mat
