# To call form command line:
# python -m unittest tests.PrintObject_tests

import unittest

from regression_runner import PrintObject

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

    def test_Print(self):
        test_message = "test message"
        self.obj.Print(test_message)
        self.obj.Print(test_message)
        self.assertEqual(self.test_stdout.data, [test_message, '\n'] * 2)
        