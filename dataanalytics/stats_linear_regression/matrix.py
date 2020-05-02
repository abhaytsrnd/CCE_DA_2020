"""Matrix
APIs
1. inverse
2. multiply
3. validate
"""
import logging
import math
import numpy as np


class Matrix:

    def __init__(self):
        logging.debug('Initialized Matrix!!')

    #TODO: Calculate Inverse without numpy
    @staticmethod
    def inverse(m: [[float]]) -> [[float]]:
        logging.debug("log: Matrix inverse Invoked.")
        Matrix.validate(m)
        npm = np.array(m)
        npm_inverse = np.linalg.inv(npm)
        m_inverse = np.asarray(npm_inverse)
        return m_inverse

    @staticmethod
    def multiply(m1: [[float]], m2:[[float]]) -> [[float]]:
        logging.debug("log: Matrix multiply Invoked.")
        Matrix.validate(m1)
        Matrix.validate(m2)

        m = len(m1)
        n1 = len(m1[0])
        n2 = len(m2)
        p = len(m2[0])
        if n1 != n2:
            raise ValueError("Matrix Multiplication does not exist!! " + str(n1) + " != "+ str(n2))

        mat = [[0.0 for x in range(p)] for x in range(m)]
        for j in range(m):
            for k in range(p):
                v = 0.0
                for q in range(n1):
                    v = v + (m1[j][q]*m2[q][k])
                mat[j][k] = v
        return mat


    @staticmethod
    def transpose(m:[[float]]) -> [[float]]:
        logging.debug("log: Matrix Transpose Invoked.")
        Matrix.validate(m)
        c = len(m)
        r = len(m[0])
        mat = [[0.0 for x in range(c)] for x in range(r)]
        for j in range (r):
            for k in range (c):
                mat[j][k] = m[k][j]
        return mat

    @staticmethod
    def validate(m:[[float]]) -> [[float]]:
        if m is None or len(m) == 0:
            raise ValueError("Matrix could not be None or Empty!!")
        if m[0] is None or len(m[0]) == 0:
            raise ValueError("Invalid Matrix!!")
        n = len(m[0])
        for col in m:
            if col is None or len(col) != n:
                raise ValueError("Invalid Matrix!!")
        return m
