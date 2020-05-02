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
from dataanalytics.stats_linear_regression.statistics import Statistics

class TestStatistics(TestCase):

    def setUp(self):
        logging.info("Setup TestStatistics!!")

    def tearDown(self):
        logging.info("TearDown TestStatistics!!")

    def test_mean(self):
        data_1 = [1,2,3,4,5,6,7,8,9]
        actual = sum(data_1)/len(data_1)
        expected = Statistics.mean(data_1)
        self.assertEqual(expected, actual)

        with self.assertRaises(TypeError):
            Statistics.mean(["a","b"])

        data_2 = [10.5,2.1,3.2,0.4,5.0000123,6.78,7.5234524,8.2654672,9.1645164]
        actual = sum(data_2)/len(data_2)
        expected = Statistics.mean(data_2)
        self.assertEqual(expected, actual)


    def test_var(self):
        data_1 = [1,2,3,4,5,6,7,8,9]
        actual = (statistics.variance(data_1),math.sqrt(statistics.variance(data_1)))
        expected = Statistics.variance(data_1)
        self.assertEqual(expected, actual)

        data_1_mean = Statistics.mean(data_1)
        actual = Statistics.variance(data_1, data_1_mean)
        self.assertEqual(expected, actual)

    def test_covariance(self):
        data_x_1 = [1,2,3,4,5,6,7,8,9]
        data_y_1 = [1,2,3,4,5,6,7,8,9]
        actual = (7.5,1)
        expected = Statistics.covariance(data_x_1, data_y_1)
        self.assertEqual(expected, actual)

        with self.assertRaises(ValueError):
            Statistics.covariance([1,2,3], [1,2])

        data_x_1_mean = Statistics.mean(data_x_1)
        data_y_1_mean = Statistics.mean(data_y_1)
        expected = Statistics.covariance(data_x_1, data_y_1, data_x_1_mean, data_y_1_mean)
        self.assertEqual(expected, actual)

    def test_correlation_coefficient(self):
        data_x_1 = [1,2,3,4,5,6,7,8,9]
        data_y_1 = [1,2,3,4,5,6,7,8,9]
        actual = 1
        expected = Statistics.correlation_coefficient(7.5, 7.5, 7.5)
        self.assertEqual(expected, actual)

    def test_describe(self):
        data = [1,2,3,4,5,6,7,8,9]
        stats = Statistics.describe(data)
        self.assertEqual(stats["count"], 9)
        self.assertEqual(stats["mean"], 5.0)
        self.assertEqual(stats["variance"], 7.5)
        self.assertEqual(stats["std"], 2.7386127875258306)
        self.assertEqual(stats["min"], 1)
        self.assertEqual(stats["max"], 9)

    ########################
    ### Validation Tests ###
    ########################

    def test_none_data(self):
        with self.assertRaises(ValueError):
            Statistics.mean(None)
        with self.assertRaises(ValueError):
            Statistics.mean([])
        with self.assertRaises(ValueError):
            Statistics.variance(None)
        with self.assertRaises(ValueError):
            Statistics.variance([])
        with self.assertRaises(ValueError):
            Statistics.covariance(None, [1])
        with self.assertRaises(ValueError):
            Statistics.covariance([], [1])
        with self.assertRaises(ValueError):
            Statistics.covariance([1], None)
        with self.assertRaises(ValueError):
            Statistics.covariance([1], [])
        with self.assertRaises(ValueError):
            Statistics.covariance([1], [1,2])

if __name__ == '__main__':
    unittest.main()
