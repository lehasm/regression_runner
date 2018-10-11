# To call form command line:
# python -m unittest tests.regression_input_tests

import unittest
import sys
import os

from regression_runner import *
from regression_runner.RunObject import *

class TestRun(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Run(self):
        test_command = "echo OK"
        self.assertIsInstance(R, RunObject)
        Run()
        self.assertEqual(R.parallel_processes, 1)
        self.assertEqual(R.parallel_groups_allowed, False)
        Run(parallel_processes = 4, parallel_groups_allowed = True, pre_commands = [test_command], post_commands = [test_command])
        self.assertEqual(R.parallel_processes, 4)
        self.assertEqual(R.parallel_groups_allowed, True)
        self.assertEqual(R.pre_commands, [test_command])
        self.assertEqual(R.post_commands, [test_command])
        with self.assertRaises(AttributeError):
            Run(log_path = "unexpected substitiution")

    def test_Substitute(self):
        R.substitutions = {}
        Substitute(irun_args = "+define+CONNECT_TEST_DRIVER")
        self.assertEqual(R.substitutions, {"irun_args": "+define+CONNECT_TEST_DRIVER"})
        
    def test_Args(self):
        sys.argv = ["run_path", "A0", "A1"]
        self.assertEqual(Args(), ["A0", "A1"])
        self.assertEqual(Args(0), "A0")
        self.assertEqual(Args(1), "A1")

    def test_Env(self):
        test_name = "TEST_ENV_VAR"
        test_value = "TEST_VALUE"
        os.environ[test_name] = test_value
        self.assertEqual(Env(test_name), test_value)
