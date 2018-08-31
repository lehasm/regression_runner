from RunDescriptionObject import RunDescriptionObject

class TestObject(RunDescriptionObject):
    """ Class to manage groups  """

    def __init__(self, name):
        super(TestObject, self).__init__(name)