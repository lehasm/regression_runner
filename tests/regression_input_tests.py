# To call form command line:
# python -m unittest tests.regression_input_tests

import unittest

from regression_runner import *


class TestRun(unittest.TestCase):

    def setUp(self):
        pass
        # print(">>> setUp()")

    def tearDown(self):
        pass
        # print(">>> tearDown()")


    def test_return_value(self):
        """ Tests are functions with special prefix "test_"
            (other variants of running tests are also exist)
        """
        self.assertTrue(Run())

