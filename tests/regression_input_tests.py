# To call form command line:
# python -m unittest tests.regression_input_tests

import unittest

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
        Substitute(irun_args = "+define+CONNECT_TEST_DRIVER")
        self.assertEqual(R.substitutions, {"irun_args": "+define+CONNECT_TEST_DRIVER"})
