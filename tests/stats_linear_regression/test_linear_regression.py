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

    def test_run_success(self):
        print("Test 1")

    def test_run_success_2(self):
        print("Test 2")

if __name__ == '__main__':
    unittest.main()
