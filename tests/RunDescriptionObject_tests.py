# To call form command line:
# python -m unittest tests.RunDescriptionObject_tests

import unittest

from regression_runner import RunDescriptionObject

def SomeFunction():
    pass


class TestRun(unittest.TestCase):

    def setUp(self):
        self.obj = RunDescriptionObject.RunDescriptionObject("RunDescriptionObject0")

    def tearDown(self):
        del self.obj

    def test_Reset(self):
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


    def test_InitFlatSubstitutions(self):
        self.obj.substitutions = {"p0": "${p1} ${p2}", "p1": "check", "p2": "this"}
        self.obj.InitFlatSubstitutions()
        self.assertEqual(self.obj.flat_substitutions, {"p0": "check this",  "p1": "check", "p2": "this"})


    def test_UpdateRunContext(self):
        self.obj.UpdateRunContext({"s0": "v0"})
        self.assertEqual(self.obj.substitutions, {"s0": "v0"})
        self.obj.UpdateRunContext({"count": 1, "s1": "v1"})
        self.assertEqual(self.obj.substitutions, {"s0": "v0", "s1": "v1"})
        self.obj.UpdateRunContext({"s0": "v0_new"})
        self.assertEqual(self.obj.substitutions, {"s0": "v0_new", "s1": "v1"})
        self.obj.UpdateRunContext({"count": 10})
        self.assertEqual(self.obj.substitutions, {"s0": "v0_new", "s1": "v1"})
        self.assertEqual(self.obj.count, 10)


    def test_ClearSubstitutions(self):
        self.obj.UpdateRunContext({"s0": "v0"})
        self.obj.ClearSubstitutions()
        self.assertEqual(self.obj.substitutions, {})


    def test_GetLogName(self):
        self.obj.name = "N"
        self.assertEqual(self.obj.GetLogName(), "N.log")
        self.obj.count = 5
        self.assertEqual(self.obj.GetLogName(0), "N_0.log")
        self.obj.count = 10
        self.assertEqual(self.obj.GetLogName(9), "N_9.log")
        self.obj.count = 110
        self.assertEqual(self.obj.GetLogName(0), "N_000.log")


    def test_RunAll(self):
        self.obj.name = "test_RunAll"
        self.obj.pre_commands = ["echo pre_commands"]
        self.obj.post_commands = ["echo post_commands"]
        self.obj._RunAll()
        self.obj.pre_commands_result.RemoveLog()
        self.obj.post_commands_result.RemoveLog()
        
