# To call form command line:
# python -m unittest tests.RunDescriptionObject_tests

import unittest

from regression_runner import RunDescriptionObject


class TestRun(unittest.TestCase):

    def setUp(self):
        self.obj = RunDescriptionObject.RunDescriptionObject()

    def tearDown(self):
        del self.obj

    def test_reset(self):
        self.obj.Reset()
        self.assertEqual(self.obj.name, "")
        self.assertEqual(self.obj.count, 1)
        self.assertEqual(self.obj.timeout, None)
        self.assertEqual(self.obj.pre_commands, [])
        self.assertEqual(self.obj.test_commands, [])
        self.assertEqual(self.obj.check_commands, [])
        self.assertEqual(self.obj.post_commands, [])

