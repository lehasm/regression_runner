# To call form command line:
# python -m unittest tests.RunObject_tests

import unittest

from regression_runner import RunObject


class TestRunObject(unittest.TestCase):

    def setUp(self):
        self.obj = RunObject.RunObject()

    def tearDown(self):
        del self.obj

    def test_dummy(self):
        self.assertTrue(True)

