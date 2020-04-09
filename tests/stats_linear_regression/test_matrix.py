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

    def test_multiply(self):
        m1 = [[1,2,3],[3,4,5],[6,7,8]]
        m2 = [[1,2,3]]
        actual = [[14.0, 26.0, 44.0]]
        expected = Matrix.multiply(m1,m2)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
