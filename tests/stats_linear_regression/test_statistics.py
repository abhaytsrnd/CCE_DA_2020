#################################
# This has to be added to find the custom packages
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
#################################
import unittest
from unittest import TestCase


import logging
from dataanalytics.stats_linear_regression.statistics import Statistics

class TestStatistics(TestCase):

    def setUp(self):
        logging.info("Setup TestStatistics!!")

    def tearDown(self):
        logging.info("TearDown TestStatistics!!")

    def test_run_success(self):
        print("Test 1")

    def test_run_success_2(self):
        print("Test 2")

if __name__ == '__main__':
    unittest.main()
