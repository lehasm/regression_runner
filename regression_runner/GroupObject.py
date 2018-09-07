
from RunDescriptionObject import RunDescriptionObject
from TestObject import TestObject

class GroupObject(RunDescriptionObject):
    """ Class to manage groups  """

    def __init__(self, name):
        super(GroupObject, self).__init__(name)
        self.tests = {}


    def AddTest(self, test):
        if (not isinstance(test, TestObject)):
            raise TypeError()
        if (test.name in self.tests):
            raise KeyError("Test name {} is already used in this group. Names must be unique.".format(test.name))
        self.tests[test.name] = test

    def __iter__(self):
        for test in self.tests.itervalues():
            for i in xrange(0, test.count):
                test.UpdateRunContext({"i": i})
                yield test