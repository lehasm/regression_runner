
class ResultObject():
    """ Class to store test run results and to manage log file """

    def __init__(self, log_file_name = None):
        self.state = "waiting"
        self.timeout = False
        self.passed = False
        self.log_file_name = log_file_name
        self._log_file = None
      
    def __del__(self):
        self.CloseLog()
            
    @property        
    def log_file(self):
        if self.log_file_name:
            self._log_file = open(self.log_file_name, "a")
        return self._log_file
        
    
    def CloseLog(self):
         if self._log_file:
            self._log_file.close()
        