
from RunDescriptionObject import RunDescriptionObject

class GroupObject(RunDescriptionObject):
    """ Class to manage groups  """

    def __init__(self, name):
        super(GroupObject, self).__init__(name)
        self.tests = {}


    def AddTest(self, test):
        if (test.name in self.tests):
            raise KeyError("Test name {} is already used in this group. Names must be unique.".format(test.name))
        self.tests[test.name] = test