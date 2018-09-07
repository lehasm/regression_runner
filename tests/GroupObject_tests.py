# To call form command line:
# python -m unittest tests.GroupObject_tests

import unittest

from regression_runner import GroupObject
from regression_runner import TestObject


class TestGroupObject(unittest.TestCase):

    def setUp(self):
        self.obj = GroupObject.GroupObject("GroupObject0")
        self._test0 = TestObject.TestObject("test0")
        self._test1 = TestObject.TestObject("test1")

    def tearDown(self):
        del self.obj

    def test_AddTest(self):
        with self.assertRaises(TypeError):
            self.obj.AddTest("invalid type")
        self.obj.AddTest(self._test0)
        self.obj.AddTest(self._test1)
        self.assertEqual(self.obj.tests, {self._test0.name: self._test0, self._test1.name: self._test1})

    def test_iter(self):
        self._test0.count = 4
        self._test1.count = 2
        ref_seq =  [("test1", i) for i in xrange(0, self._test1.count)]
        ref_seq += [("test0", i) for i in xrange(0, self._test0.count)]
        gen_seq = []
        self.obj.AddTest(self._test0)
        self.obj.AddTest(self._test1)
        for t in self.obj:
            gen_seq.append( (t.name, t.substitutions["i"]) )
        self.assertEqual(gen_seq, ref_seq)