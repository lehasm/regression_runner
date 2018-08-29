class RunDescriptionObject(object):
    """ Data and functions common to any level: test, group, global run. """

    def Reset(self):
        self.name                = ""
        self.count               = 1
        self.timeout             = None

        self.pre_commands        = []
        self.test_commands       = []
        self.check_commands      = []
        self.post_commands       = []

        def __init__(self):
            self.Reset()