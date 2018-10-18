# To call form command line:
# python -m unittest tests.ResultObject_tests

import unittest
import os

class TestResultObject(unittest.TestCase):

    def setUp(self):
        self.log_name = "test_ResultObject.log"
        self.obj = ResultObject.ResultObject(self.log_name)

    def tearDown(self):
        self.obj.RemoveLog()

    