# To call form command line:
# python -m unittest tests.run_facilities_tests

import unittest

from regression_runner.run_facilities import *
import os


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
        with open(temp_name, 'w') as f:
            self.assertEqual(RunCommands(["echo " + test_string], f), [0])
        with open(temp_name, 'r') as f:
            f_content = f.read()
            self.assertEqual(f_content, test_string + "\n")
        os.remove(temp_name)