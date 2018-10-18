# To call form command line:
# python -m unittest tests.run_facilities_tests

import unittest
import os

from regression_runner.run_facilities import *
from regression_runner.ResultObject import ResultObject


class TestRun(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_RunCommands(self):
        return_codes = [0, 1, 255]
        commands = ["exit {}".format(r) for r in return_codes]
        self.assertEqual(RunCommands(commands, None), return_codes)

        temp_name = "test_RunCommands.log"
        test_string = "test"
        self.assertEqual(RunCommands(["echo " + test_string], temp_name), [0])
        with open(temp_name, 'r') as f:
            f_content = f.read()
            f.close()
            os.remove(temp_name)
            self.assertEqual(f_content, 
                "\n> echo {0}\n{0}\n".format(test_string))
            
        
    def test_RunCommandsWithTimeout(self):
        test_result = ResultObject("test.log")
        timeout = 1
        return_codes = [0, 1, 255]
        commands = ["exit {}".format(r) for r in return_codes]
        RunCommandsWithTimeout(commands, timeout, test_result)
        self.assertEqual(test_result.return_codes, return_codes)
        self.assertEqual(test_result.timeout, False)
        
        RunCommandsWithTimeout(["sleep {}".format(timeout + 1)], timeout, test_result)
        self.assertEqual(test_result.timeout, True)
        
