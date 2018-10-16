
class TestResultObject():
    """ Class to store test run results  """

    def __init__(self, name, log_file_name = None):
        self.state = "waiting"
        self.timeout = False
        self.passed = False
        self.log_file = open(log_file_name) if log_file_name else None
        