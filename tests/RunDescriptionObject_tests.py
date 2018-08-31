# To call form command line:
# python -m unittest tests.RunDescriptionObject_tests

import unittest

from regression_runner import RunDescriptionObject

def SomeFunction():
    pass


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

    def testNormalizeCommands(self):
        self.assertEqual(self.obj.NormalizeCommands(["echo 1", "echo 2"]), ["echo 1", "echo 2"])
        self.assertEqual(self.obj.NormalizeCommands("echo 1"), ["echo 1"])
        self.assertEqual(self.obj.NormalizeCommands(SomeFunction), [SomeFunction])
        self.assertEqual(self.obj.NormalizeCommands([SomeFunction, SomeFunction]), [SomeFunction, SomeFunction])
        with self.assertRaises(TypeError):
            self.obj.NormalizeCommands(0)
        with self.assertRaises(TypeError):
            self.obj.NormalizeCommands(["echo 3", (1, 2, 3)])

        self.obj.pre_commands       = "echo Go"
        self.obj.test_commands      = "irun"
        self.obj.check_commands     = SomeFunction
        self.obj.post_commands      = "echo Done"
        self.obj.NormalizeAllCommands()
        self.assertEqual(self.obj.pre_commands  , ["echo Go"]   )
        self.assertEqual(self.obj.test_commands , ["irun"]      )
        self.assertEqual(self.obj.check_commands, [SomeFunction])
        self.assertEqual(self.obj.post_commands , ["echo Done"] )

    def test_RaiseIfRecursiveSubstitution(self):
        self.obj.RaiseIfRecursiveSubstitution("p0", "( ${p1})")     # no exception
        with self.assertRaises(KeyError):
            self.obj.RaiseIfRecursiveSubstitution("p1", "recursive ${p1}")

    def test_FlattenSubstitutions(self):
        self.assertEqual(self.obj.FlattenSubstitutions({"p0": "${p1} ${p2}", "p1": "check", "p2": "this"}),
                                                       {"p0": "check this",  "p1": "check", "p2": "this"})

        self.assertEqual(self.obj.FlattenSubstitutions({"p0": "${p1} ${p2}", "p1": "${p2}", "p2": "this"}),
                                                       {"p0": "this this",  "p1": "this", "p2": "this"})

        with self.assertRaises(KeyError):
            self.obj.FlattenSubstitutions({"p0": "${p1} ${p2}", "p1": "check"})
        with self.assertRaises(KeyError):
            self.obj.FlattenSubstitutions({"p0": "${p1}", "p1": "${p2}", "p2": "${p0}"})
        with self.assertRaises(KeyError):
            self.obj.FlattenSubstitutions({"p0": "${p1} ${p1}", "p1": "${p2}", "p2": "${p1}"})