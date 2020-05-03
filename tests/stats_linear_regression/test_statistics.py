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


    ###################################
    #### Partial Correlation Tests ####
    ###################################

    def test_yule_walker1(self):
        r12_3 = Statistics.yule_walker_eq(0.819, 0.774, 0.802)
        self.assertEqual(r12_3, 0.5241753109234627)

    def test_yule_walker2(self):
        r12_3 = Statistics.yule_walker_eq(0.774, 0.819, 0.802)
        self.assertEqual(r12_3, 0.3418386394082465)

    def test_partial_correlation1(self):
        y = [64,71,53,67,55,58,77,57,56,51,76,68]
        x1 = [57,59,49,62,51,50,55,48,52,42,61,57]
        x2 = [8,10,6,11,8,7,10,9,10,6,12,9]
        ry1_2 = Statistics.partial_correlation(y, x1, [x2])
        ry1_2 = round(ry1_2 , 3)
        self.assertEqual(ry1_2, 0.533)

    def test_partial_correlation2(self):
        y = [64,71,53,67,55,58,77,57,56,51,76,68]
        x1 = [57,59,49,62,51,50,55,48,52,42,61,57]
        x2 = [8,10,6,11,8,7,10,9,10,6,12,9]
        ry2_1 = Statistics.partial_correlation(y, x2, [x1])
        ry2_1 = round(ry2_1 , 3)
        self.assertEqual(ry2_1, 0.335)

    def test_partial_correlation_4data(self):
        x1 = [75,83,85,85,92,97,99]
        x2 = [1.85, 1.25, 1.5, 1.75, 1.15, 1.75, 1.6]
        x3 = [16,20,25,27,32,48,48]
        x4 = [14,21,29,16,21,47,47]
        r12_34 = Statistics.partial_correlation(x1, x2, [x3, x4])
        r12_34 = round(r12_34 , 3)
        self.assertEqual(r12_34, -0.961)

    def test_correlation_matrix_4data(self):
        x1 = [75,83,85,85,92,97,99]
        x2 = [1.85, 1.25, 1.5, 1.75, 1.15, 1.75, 1.6]
        x3 = [16,20,25,27,32,48,48]
        x4 = [14,21,29,16,21,47,47]
        mat = Statistics.correlation_matrix([x1, x2, x3, x4])
        actual = [[1.0, -0.15534261150561485, 0.9627972334240521, 0.8520652907262152], [-0.15534261150561485, 1.0, 0.10551846545168846, 0.13506331370887886], [0.9627972334240521, 0.10551846545168846, 1.0, 0.9088795720039011], [0.8520652907262152, 0.13506331370887886, 0.9088795720039011, 1.0]]
        self.assertEqual(mat, actual)

    def test_partial_correlation_matrix_4data(self):
        x1 = [75,83,85,85,92,97,99]
        x2 = [1.85, 1.25, 1.5, 1.75, 1.15, 1.75, 1.6]
        x3 = [16,20,25,27,32,48,48]
        x4 = [14,21,29,16,21,47,47]
        mat = Statistics.partial_correlation_matrix([x1, x2, x3, x4])
        actual = [[1.0, -0.9613273119340023, 0.9866069072448754, -0.3903841491779091], [-0.9613273119340022, 1.0, 0.9465782218637125, -0.3513457030175387], [0.9866069072448754, 0.9465782218637125, 1.0, 0.5215083165976273], [-0.3903841491779091, -0.35134570301753876, 0.5215083165976273, 1.0]]
        self.assertEqual(mat, actual)

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

    def test_yule_walker_none_data(self):
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(None, 0.774, 0.802)
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(1, None, 0.802)
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(1, 0.774, None)
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(1.2, 0.774, 0.802)
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(1, 1.2, 0.802)
        with self.assertRaises(ValueError):
            Statistics.yule_walker_eq(1, 0.774, -1.2)

    def test_partial_correlation_none_data(self):
        with self.assertRaises(ValueError):
            Statistics.partial_correlation(None, [1],[[2]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], None,[[2]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], [1],None)
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([], [1],[[1]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], [],[[1]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], [1],[[]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], [1],[[1,2]])
        with self.assertRaises(ValueError):
            Statistics.partial_correlation([1], [1,2],[[1,2]])

if __name__ == '__main__':
    unittest.main()
