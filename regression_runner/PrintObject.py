"""
Outputs run information
"""

from RunObject import RunObject 

class PrintObject:

    def __init__(self):
        pass

            
    def PrintFunction(self, message):
        print(message)
        
        
    def PrintSessionHeader(self, r):
        if (not isinstance(r, RunObject)):
            raise TypeError()
        self.PrintFunction("""
        #Session header
        {}
        """.format(r))