# To call form command line:
# python -m unittest tests.RunObject_tests

import unittest

from regression_runner import RunObject


class TestRunObject(unittest.TestCase):

    def setUp(self):
        self.obj = RunObject.RunObject("RunObject0")

    def tearDown(self):
        del self.obj

    def test_Init(self):
        self.assertEqual(self.obj.parallel_processes, 1)
        self.assertEqual(self.obj.parallel_groups_allowed, False)

    def test_AddDefaultSubstitutions(self):
        self.assertIn("time_tag", self.obj.substitutions)
        self.obj.substitutions["time_tag"] = ""
        self.assertEqual(self.obj.substitutions, 
            {
                "log_path" : "./logs/${time_tag}",
                "time_tag" : "",    # has been overriden above
            })
        

