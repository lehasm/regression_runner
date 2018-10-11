"""
Outputs run progress. May be called from different processes
"""

from multiprocessing import Lock


class PrintObject:

    def __init__(self):
        self.lock = Lock()

        
    def Print(self, message):
        self.lock.acquire()
        self.PrintFunction(message)
        self.lock.release()
        
    def PrintFunction(self, message):
        print(message)
        