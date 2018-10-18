
class ResultObject():
    """ Class to store test run results  """

    def __init__(self, log_file_name = None):
        self.state = "waiting"
        self.timeout = False
        self.passed = False
        self.log_file = open(log_file_name, "a") if log_file_name else None
        