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
        actual_stats = [{'count': 10, 'mean': 262.881, 'variance': 47312.01869888888, 'std': 217.51326097249537, 'min': 7.5, 'max': 698.88, 'covariance': 47312.01869888888, 'r': 1.0, 'pr': 1.0}, {'count': 10, 'mean': 5.5, 'variance': 9.166666666666666, 'std': 3.0276503540974917, 'min': 1, 'max': 10, 'covariance': 633.3694444444444, 'r': 0.9617576489183196, 'pr': 0.9617576489183195}]
        actual_ycap = [-48.045818181817964, 21.04903030303052, 90.143878787879, 159.2387272727275, 228.333575757576, 297.42842424242446, 366.5232727272729, 435.6181212121214, 504.71296969696994, 573.8078181818184]

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), self.round(actual_params,5))
        self.assertEqual(self.round(ycap, 5), self.round(actual_ycap, 5))
        self.assertEqual(model.stats(), actual_stats)
        self.assertEqual(model.params(), actual_params)
        self.assertEqual(model.predicts(data), actual_ycap)
        self.assertEqual(model.predict([1]), -48.045818181817964)
        self.assertEqual(self.round(model.ycap(), 5), self.round(actual_ycap, 5))

        actual_corr = [[1.0, 0.9617576489183196], [0.9617576489183196, 1.0]]
        actual_partial_corr = [[1.0, 0.9617576489183195], [0.9617576489183195, 1.0]]
        self.assertEqual(model.correlation_matrix(), actual_corr)
        self.assertEqual(model.partial_correlation_matrix(), actual_partial_corr)

        model_stats = model.model_stats()
        self.assertEqual(round(model_stats['mean'], 4), 0)

    def test_linear_model_linear_fit_120(self):
        data = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]]
        y = [7.5, 44.31, 60.8, 148.97, 225.5, 262.64, 289.06, 451.53, 439.62, 698.88, 748.24, 896.46, 1038.78, 1214.04, 1377.08, 1579.86, 1763.14, 1993.92, 2196.96, 2456.22, 2678.54, 2966.76, 3207.88, 3525.54, 3784.98, 4132.56, 4409.84, 4787.82, 5082.46, 5491.32, 5802.84, 6243.06, 6570.98, 7043.04, 7386.88, 7891.26, 8250.54, 8787.72, 9161.96, 9732.42, 10121.14, 10725.36, 11128.08, 11766.54, 12182.78, 12855.96, 13285.24, 13993.62, 14435.46, 15179.52, 15633.44, 16413.66, 16879.18, 17696.04, 18172.68, 19026.66, 19513.94, 20405.52, 20902.96, 21832.62, 22339.74, 23307.96, 23824.28, 24831.54, 25356.58, 26403.36, 26936.64, 28023.42, 28564.46, 29691.72, 30240.04, 31408.26, 31963.38, 33173.04, 33734.48, 34986.06, 35553.34, 36847.32, 37419.96, 38756.82, 39334.34, 40714.56, 41296.48, 42720.54, 43306.38, 44774.76, 45364.04, 46877.22, 47469.46, 49027.92, 49622.64, 51226.86, 51823.58, 53474.04, 54072.28, 55769.46, 56368.74, 58113.12, 58712.96, 60505.02, 61104.94, 62945.16, 63544.68, 65433.54, 66032.18, 67970.16, 68567.44, 70555.02, 71150.46, 73188.12, 73781.24, 75869.46, 76459.78, 78599.04, 79186.08, 81376.86, 81960.14, 84202.92, 84781.96, 87077.22]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [728.0277472393905, -14756.466124649785]
        actual_stats = [{'count': 120, 'mean': 29289.212583333345, 'variance': 683257156.1909251, 'std': 26139.188131824696, 'min': 7.5, 'max': 87077.22, 'covariance': 683257156.1909251, 'r': 1.0, 'pr': 1.0}, {'count': 120, 'mean': 60.5, 'variance': 1210.0, 'std': 34.785054261852174, 'min': 1, 'max': 120, 'covariance': 880913.5741596639, 'r': 0.9688321061901478, 'pr': 0.9688321061901478}]

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), self.round(actual_params,5))
        self.assertEqual(model.stats(), actual_stats)
        self.assertEqual(model.params(), actual_params)


    def test_linear_model_bivariate_fit(self):
        data = [[14.0, 10.0, 14.0, 16.0, 10.0, 10.0, 14.0, 16.0], [4.0, 2.0, 1.0, 1.0, 4.0, 3.0, 3.0, 4.0]]
        y = [82.0, 48.0, 60.0, 85.0, 72.0, 62.0, 90.0, 101.0]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [5.735074626865639, 7.820895522388071, -21.06343283582055]
        actual_stats = [{'count': 8, 'mean': 75.0, 'variance': 311.7142857142857, 'std': 17.65543218712829, 'min': 48.0, 'max': 101.0, 'covariance': 311.7142857142857, 'r': 1.0, 'pr': 1.0}, {'count': 8, 'mean': 13.0, 'variance': 6.857142857142857, 'std': 2.6186146828319083, 'min': 10.0, 'max': 16.0, 'covariance': 34.857142857142854, 'r': 0.7539487656439327, 'pr': 0.9250084450019057}, {'count': 8, 'mean': 2.75, 'variance': 1.6428571428571428, 'std': 1.2817398889233114, 'min': 1.0, 'max': 4.0, 'covariance': 9.571428571428571, 'r': 0.42295923256718326, 'pr': 0.8516666901452074}]
        actual_ycap = [90.51119402985069, 51.929104477611986, 67.04850746268647, 78.51865671641775, 67.57089552238813, 59.75000000000006, 82.69029850746261, 101.98134328358196]

        actual_params = self.round(actual_params, 5)
        actual_ycap = self.round(actual_ycap, 5)

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), actual_params)
        self.assertEqual(self.round(ycap, 5), actual_ycap)
        self.assertEqual(self.round(model.ycap(), 5), self.round(actual_ycap, 5))

        predicts = model.predicts(data)
        predicts = self.round(predicts, 5)
        self.assertEqual(predicts, actual_ycap)

        predict = model.predict([15,5])
        predict = round(predict, 5)
        self.assertEqual(predict, 104.06716)

        actual_corr = [[1.0, 0.7539487656439327, 0.42295923256718326], [0.7539487656439327, 1.0, -0.17025130615174972], [0.42295923256718326, -0.17025130615174972, 1.0]]
        actual_partial_corr = [[1.0, 0.9250084450019057, 0.8516666901452074], [0.9250084450019057, 1.0, -0.8216999738583994], [0.8516666901452074, -0.8216999738583994, 1.0]]
        self.assertEqual(model.correlation_matrix(), actual_corr)
        self.assertEqual(model.partial_correlation_matrix(), actual_partial_corr)

        model_stats = model.model_stats()
        self.assertEqual(round(model_stats['mean'], 4), 0)

    def test_linear_model_trivariate_fit(self):
        data = [[14.0, 10.0, 14.0, 16.0, 10.0, 10.0, 14.0, 16.0], [4.0, 2.0, 1.0, 1.0, 4.0, 3.0, 3.0, 4.0], [40.0, 40.0, 50.0, 50.0, 50.0, 40.0, 50.0, 60.0]]
        y = [82.0, 48.0, 60.0, 85.0, 72.0, 62.0, 90.0, 101.0]

        model = LinearRegression()
        (stats, params, ycap) = model.fit(data, y)

        actual_params = [4.945255474452566, 7.350364963503694, 0.4503649635036453, -30.894160583940902]
        actual_stats = [{'count': 8, 'mean': 75.0, 'variance': 311.7142857142857, 'std': 17.65543218712829, 'min': 48.0, 'max': 101.0, 'covariance': 311.7142857142857, 'r': 1.0, 'pr': 1.0}, {'count': 8, 'mean': 13.0, 'variance': 6.857142857142857, 'std': 2.6186146828319083, 'min': 10.0, 'max': 16.0, 'covariance': 34.857142857142854, 'r': 0.7539487656439327, 'pr': 0.8690424878183447}, {'count': 8, 'mean': 2.75, 'variance': 1.6428571428571428, 'std': 1.2817398889233114, 'min': 1.0, 'max': 4.0, 'covariance': 9.571428571428571, 'r': 0.42295923256718326, 'pr': 0.8508196834899874}, {'count': 8, 'mean': 47.5, 'variance': 50.0, 'std': 7.0710678118654755, 'min': 40.0, 'max': 60.0, 'covariance': 84.28571428571429, 'r': 0.675134989581633, 'pr': 0.4004406241270938}]
        actual_ycap = [85.7554744525556, 51.27372262773795, 68.20802919708098, 78.0985401459861, 70.4781021897818, 58.62408759124165, 82.90875912408836, 104.65328467153364]

        actual_params = self.round(actual_params, 5)
        actual_ycap = self.round(actual_ycap, 5)

        self.assertEqual(stats, actual_stats)
        self.assertEqual(self.round(params, 5), actual_params)
        self.assertEqual(self.round(ycap, 5), actual_ycap)
        self.assertEqual(self.round(model.ycap(), 5), self.round(actual_ycap, 5))

        predicts = model.predicts(data)
        predicts = self.round(predicts, 5)
        self.assertEqual(predicts, actual_ycap)

        predict = model.predict([15,5,35])
        predict = round(predict, 5)
        self.assertEqual(predict, 95.79927)

        actual_corr = [[1.0, 0.7539487656439327, 0.42295923256718326, 0.675134989581633], [0.7539487656439327, 1.0, -0.17025130615174972, 0.6172133998483676], [0.42295923256718326, -0.17025130615174972, 1.0, 0.07881104062391008], [0.675134989581633, 0.6172133998483676, 0.07881104062391008, 1.0]]
        actual_partial_corr = [[1.0, 0.8690424878183447, 0.8508196834899874, 0.4004406241270938], [0.8690424878183448, 1.0, -0.8119486273269884, -0.05696928063170212], [0.8508196834899874, -0.8119486273269885, 1.0, -0.2265003655587716], [0.40044062412709386, -0.05696928063170224, -0.22650036555877173, 1.0]]
        self.assertEqual(model.correlation_matrix(), actual_corr)
        self.assertEqual(model.partial_correlation_matrix(), actual_partial_corr)

        model_stats = model.model_stats()
        self.assertEqual(round(model_stats['mean'], 4), 0)

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
