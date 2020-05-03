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

    def round(self, data:[float], d: int) -> [float]:
        n = len(data)
        nd = [0.0 for x in range(n)]
        for i in range(n):
            nd[i] = round(data[i], d)
        return nd

    def test_linear_model_linear_fit(self):
        data = [[1,2,3,4,5,6,7,8,9,10]]
        y = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [69.09484848484848, -117.14066666666645]
        actual_stats = [{'count': 10, 'mean': 262.881, 'variance': 47312.01869888888, 'std': 217.51326097249537, 'min': 7.5, 'max': 698.88, 'covariance': 47312.01869888888, 'r': 1.0, 'key': 'y', 'pr': 1.0}, {'count': 10, 'mean': 5.5, 'variance': 9.166666666666666, 'std': 3.0276503540974917, 'min': 1, 'max': 10, 'covariance': 633.3694444444444, 'r': 0.9617576489183196, 'key': 'x1', 'pr': 0.9617576489183195}]
        actual_ycap = [-48.045818181817964, 21.04903030303052, 90.143878787879, 159.2387272727275, 228.333575757576, 297.42842424242446, 366.5232727272729, 435.6181212121214, 504.71296969696994, 573.8078181818184]

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), self.round(actual_params,5))
        self.assertEqual(self.round(ycap, 5), self.round(actual_ycap, 5))
        self.assertEqual(model.stats(), actual_stats)
        self.assertEqual(model.params(), actual_params)
        self.assertEqual(model.predicts(data), actual_ycap)
        self.assertEqual(model.predict([1]), -48.045818181817964)

    def test_linear_model_bivariate_fit(self):
        data = [[14.0, 10.0, 14.0, 16.0, 10.0, 10.0, 14.0, 16.0], [4.0, 2.0, 1.0, 1.0, 4.0, 3.0, 3.0, 4.0]]
        y = [82.0, 48.0, 60.0, 85.0, 72.0, 62.0, 90.0, 101.0]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [5.735074626865639, 7.820895522388071, -21.06343283582055]
        actual_stats = [{'count': 8, 'mean': 75.0, 'variance': 311.7142857142857, 'std': 17.65543218712829, 'min': 48.0, 'max': 101.0, 'covariance': 311.7142857142857, 'r': 1.0, 'key': 'y', 'pr': 1.0}, {'count': 8, 'mean': 13.0, 'variance': 6.857142857142857, 'std': 2.6186146828319083, 'min': 10.0, 'max': 16.0, 'covariance': 34.857142857142854, 'r': 0.7539487656439327, 'key': 'x1', 'pr': 0.9250084450019057}, {'count': 8, 'mean': 2.75, 'variance': 1.6428571428571428, 'std': 1.2817398889233114, 'min': 1.0, 'max': 4.0, 'covariance': 9.571428571428571, 'r': 0.42295923256718326, 'key': 'x2', 'pr': 0.8516666901452074}]
        actual_ycap = [90.51119402985069, 51.929104477611986, 67.04850746268647, 78.51865671641775, 67.57089552238813, 59.75000000000006, 82.69029850746261, 101.98134328358196]

        actual_params = self.round(actual_params, 5)
        actual_ycap = self.round(actual_ycap, 5)

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), actual_params)
        self.assertEqual(self.round(ycap, 5), actual_ycap)

        predicts = model.predicts(data)
        predicts = self.round(predicts, 5)
        self.assertEqual(predicts, actual_ycap)

        predict = model.predict([15,5])
        predict = round(predict, 5)
        self.assertEqual(predict, 104.06716)

    def test_linear_model_trivariate_fit(self):
        data = [[14.0, 10.0, 14.0, 16.0, 10.0, 10.0, 14.0, 16.0], [4.0, 2.0, 1.0, 1.0, 4.0, 3.0, 3.0, 4.0], [40.0, 40.0, 50.0, 50.0, 50.0, 40.0, 50.0, 60.0]]
        y = [82.0, 48.0, 60.0, 85.0, 72.0, 62.0, 90.0, 101.0]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [4.945255474452566, 7.350364963503694, 0.4503649635036453, -30.894160583940902]
        actual_stats = [{'count': 8, 'mean': 75.0, 'variance': 311.7142857142857, 'std': 17.65543218712829, 'min': 48.0, 'max': 101.0, 'covariance': 311.7142857142857, 'r': 1.0, 'key': 'y', 'pr': 1.0}, {'count': 8, 'mean': 13.0, 'variance': 6.857142857142857, 'std': 2.6186146828319083, 'min': 10.0, 'max': 16.0, 'covariance': 34.857142857142854, 'r': 0.7539487656439327, 'key': 'x1', 'pr': 0.8690424878183447}, {'count': 8, 'mean': 2.75, 'variance': 1.6428571428571428, 'std': 1.2817398889233114, 'min': 1.0, 'max': 4.0, 'covariance': 9.571428571428571, 'r': 0.42295923256718326, 'key': 'x2', 'pr': 0.8508196834899874}, {'count': 8, 'mean': 47.5, 'variance': 50.0, 'std': 7.0710678118654755, 'min': 40.0, 'max': 60.0, 'covariance': 84.28571428571429, 'r': 0.675134989581633, 'key': 'x3', 'pr': 0.4004406241270938}]
        actual_ycap = [85.7554744525556, 51.27372262773795, 68.20802919708098, 78.0985401459861, 70.4781021897818, 58.62408759124165, 82.90875912408836, 104.65328467153364]

        actual_params = self.round(actual_params, 5)
        actual_ycap = self.round(actual_ycap, 5)

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), actual_params)
        self.assertEqual(self.round(ycap, 5), actual_ycap)

        predicts = model.predicts(data)
        predicts = self.round(predicts, 5)
        self.assertEqual(predicts, actual_ycap)

        predict = model.predict([15,5,35])
        predict = round(predict, 5)
        self.assertEqual(predict, 95.79927)

    ########################
    ### Validation Tests ###
    ########################

    def test_linear_model_none_independent_variables(self):
        model = LinearRegression()
        with self.assertRaises(ValueError):
            model.fit(None, [1])
        with self.assertRaises(ValueError):
            model.fit([], [1])

    def test_linear_model_none_dependent_variables(self):
        model = LinearRegression()
        with self.assertRaises(ValueError):
            model.fit([[1]], None)
        with self.assertRaises(ValueError):
            model.fit([[1]], [])

    def test_linear_model_corrupted_independent_variables(self):
        model = LinearRegression()
        with self.assertRaises(ValueError):
            model.fit([[1,2]], [1])
        with self.assertRaises(ValueError):
            model.fit([[1]], [1,2])
        with self.assertRaises(ValueError):
            model.fit([[1,2], [1]], [1,2])

    def test_linear_model_no_of_data_points_mismatch(self):
        model = LinearRegression()
        with self.assertRaises(ValueError):
            model.fit([[1,2], [1,2]], [1,2,3])



if __name__ == '__main__':
    unittest.main()
