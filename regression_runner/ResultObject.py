
import os, os.path

class ResultObject():
    """ Class to store test run results and to manage log file """

    def __init__(self, log_file_name = None):
        self.state = "waiting"
        self.timeout = False
        self.passed = False
        self.log_file_name = log_file_name
    
        
    def RemoveLog(self):
         if self.log_file_name and os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)
        