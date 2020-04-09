#################################
# This has to be added to find the custom packages
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
#################################
import unittest
from unittest import TestCase

import logging
from dataanalytics.stats_linear_regression.linear_regression import LinearRegression

class TestLinearRegression(TestCase):

    def setUp(self):
        logging.info("Setup TestLinearRegression!!")

    def tearDown(self):
        logging.info("TearDown TestLinearRegression!!")

    def test_linear_model_bivariate(self):
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]
        data = [x]
        actual = [69.09484848484848, -117.14066666666645]
        expected = LinearRegression.model(data, y)
        self.assertEqual(expected, actual)

        #with self.assertRaises(TypeError):
        #    Statistics.mean(["a","b"])

if __name__ == '__main__':
    unittest.main()
