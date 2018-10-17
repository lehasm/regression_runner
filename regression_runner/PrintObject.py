"""
Outputs run information
"""

import RunObject, GroupObject, TestObject 

class PrintObject:

    def __init__(self):
        pass

            
    def PrintFunction(self, message):
        print(message)
        
        
    def PrintSessionHeader(self, r):
        if (not isinstance(r, RunObject.RunObject)):
            raise TypeError()
        self.PrintFunction("""
        #Session header
        {}
        """.format(r))