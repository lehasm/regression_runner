
class TestResultObject():
    """ Class to store test run results  """

    def __init__(self, name, log_file_name):
        self.state = "waiting"
        self.timout = False
        self.passed = False
        self.log_file = open(log_file_name)
        