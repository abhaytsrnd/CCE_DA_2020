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

    def test_linear_model_bivariate_fit(self):
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]
        data = [x]
        actual_params = [69.09484848484848, -117.14066666666645]
        actual_stats = [{'count': 10, 'mean': 5.5, 'variance': 9.166666666666666, 'std': 3.0276503540974917, 'min': 1, 'max': 10, 'covariance': 633.3694444444444, 'r': 0.9617576489183196}, {'count': 10, 'mean': 262.881, 'variance': 47312.01869888888, 'std': 217.51326097249537, 'min': 7.5, 'max': 698.88, 'covariance': 47312.01869888888, 'r': 1}]
        actual_ycap = [-48.045818181817964, 21.04903030303052, 90.143878787879, 159.2387272727275, 228.333575757576, 297.42842424242446, 366.5232727272729, 435.6181212121214, 504.71296969696994, 573.8078181818184]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        self.assertEqual(stats, actual_stats)
        self.assertEqual(params, actual_params)
        self.assertEqual(ycap, actual_ycap)
        self.assertEqual(model.stats(), actual_stats)
        self.assertEqual(model.predicts(data), actual_ycap)
        self.assertEqual(model.predict([1]), -48.045818181817964)


        #with self.assertRaises(TypeError):
        #    Statistics.mean(["a","b"])

    def test_linear_model_bivariate_predict(self):
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]
        data = [x]
        #model = LinearRegression()
        #model.fit(data, y)
        #print(expected)

if __name__ == '__main__':
    unittest.main()
