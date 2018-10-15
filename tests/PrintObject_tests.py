# To call form command line:
# python -m unittest tests.PrintObject_tests

import unittest

from regression_runner import PrintObject, RunObject

import sys


class TestPrintObject(unittest.TestCase):

    class PrintInterceptor:
        def __init__(self):
            self.data = []

        def write(self, s):
            self.data.append(s)

        def __str__(self):
            return "".join(self.data)


    def setUp(self):
        self.obj = PrintObject.PrintObject()
        self.test_stdout = TestPrintObject.PrintInterceptor()
        sys.stdout = self.test_stdout

    def tearDown(self):
        del self.obj

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            self.obj.PrintSessionHeader(self)
        self.obj.PrintSessionHeader(RunObject.RunObject(""))