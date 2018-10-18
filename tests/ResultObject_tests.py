# To call form command line:
# python -m unittest tests.ResultObject_tests

import unittest
import os
from multiprocessing import Process

from regression_runner import ResultObject


def AccessFile(r):
    r.log_file.write("access\n")
    r.CloseLog()
    pass
    

class TestResultObject(unittest.TestCase):

    def setUp(self):
        self.log_name = "test_ResultObject.log"
        self.obj = ResultObject.ResultObject(self.log_name)
        self.obj.log_file.write("")
        self.obj.CloseLog()

    def tearDown(self):
        os.remove(self.log_name)

    def test_nolog(self):
        temp = ResultObject.ResultObject()
        del temp

    def test_from_different_process(self):
        p = Process(target = AccessFile, args = (self.obj,))
        p.start()
        p.join()
        with open(self.log_name) as f:
            self.assertEqual(f.read(), "access\n")
        
