#################################
# This has to be added to find the custom packages
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
#################################
import unittest
from unittest import TestCase


import logging
import statistics
import math
from dataanalytics.stats_linear_regression.matrix import Matrix

class TestMatrix(TestCase):

    def setUp(self):
        logging.info("Setup TestMatrix!!")

    def tearDown(self):
        logging.info("TearDown TestMatrix!!")

    def test_addition_2corss2_m1_m2(self):
        m1 = [[1,2],[3,4]]
        m2 = [[5,6],[0,-2]]
        actual = [[6,8],[3,2]]
        expected = Matrix.add(m1,m2)
        self.assertEqual(expected, actual)

    def test_scalar_multiply_square_2corss2_m1_m2(self):
        m1 = [[1,2],[3,4]]
        s = 5
        actual = [[5,10],[15,20]]
        expected = Matrix.scalar_multiply(m1,s)
        self.assertEqual(expected, actual)

    def test_multiply_square_2corss2_m1_m2(self):
        m1 = [[1,2],[3,4]]
        m2 = [[5,6],[0,-2]]
        actual = [[5,2],[15,10]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)

    def test_multiply_square_2cross2_m2_m1(self):
        m1 = [[1,2],[3,4]]
        m2 = [[5,6],[0,-2]]
        actual = [[23,34],[-6,-8]]
        expected = Matrix.multiply(m2,m1)
        self.assertEqual(expected, actual)

    def test_multiply1(self):
        m1 = [[1,2,3],[4,5,6]]
        m2 = [[7,8],[9,10],[11,12]]
        actual = [[58, 64],[139,154]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)

    def test_multiply2(self):
        m1 = [[3,2,1,5],[9,1,3,0]]
        m2 = [[2,9,0],[1,3,5],[2,4,7],[8,1,5]]
        actual = [[50,42,42],[25,96,26]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)

    def test_multiply3(self):
        m1 = [[1,4,6]]
        m2 = [[2,3], [5,8], [7,9]]
        actual = [[64,89]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)

    def test_multiply_single(self):
        m1 = [[5]]
        m2 = [[5]]
        actual = [[25]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)

    def test_multiply_not_exist(self):
        m1 = [[1,2,3]]
        m2 = [[1,2,3],[3,4,5],[6,7,8]]
        with self.assertRaises(ValueError):
            Matrix.multiply(m2,m1)


    def test_col_to_row_transform(self):
        m1 = [[1,2,3],[4,5,6]]
        actual = [[1,4], [2,5], [3,6]]
        expected = Matrix.transpose(m1)
        self.assertEqual(expected, actual)

    def test_row_to_col_transform(self):
        m1 = [[1,4], [2,5], [3,6]]
        actual = [[1,2,3],[4,5,6]]
        expected = Matrix.transpose(m1)
        self.assertEqual(expected, actual)

    def test_square_transform(self):
        m1 = [[1,2,3],[4,5,6], [7,8,9]]
        actual = [[1,4,7], [2,5,8], [3,6,9]]
        expected = Matrix.transpose(m1)
        self.assertEqual(expected, actual)

    def test_identity(self):
        m = 3
        actual = [[1,0,0], [0,1,0], [0,0,1]]
        expected = Matrix.identity(m)
        self.assertEqual(expected, actual)

    ########################
    ### Validation Tests ###
    ########################
    def test_matrix_validation(self):
        with self.assertRaises(ValueError):
            Matrix.validate([])
        with self.assertRaises(ValueError):
            Matrix.validate(None)
        with self.assertRaises(ValueError):
            Matrix.validate([None, [1]])
        with self.assertRaises(ValueError):
            Matrix.validate([[], [1]])
        with self.assertRaises(ValueError):
            Matrix.validate([[1], None])
        with self.assertRaises(ValueError):
            Matrix.validate([[1], []])
        with self.assertRaises(ValueError):
            Matrix.validate([[1,2], [1]])
        with self.assertRaises(ValueError):
            Matrix.validate([[1,2], [1,2,3]])


if __name__ == '__main__':
    unittest.main()
