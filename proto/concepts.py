import sys

print """
=== Logging ==="""
import logging

logging.basicConfig(level=logging.INFO,
                    filename='example.log', filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
#
logging.info('info message')
logging.warn('warn message')
logging.error('error message')


print """
=== Arguments ==="""

def Args(i = None):
    if (i is None):
        return sys.argv[1:]
    elif (0 <= i < len(sys.argv)-1):
        return sys.argv[1 + i]
    else:    
        return ""

print "Script args:", Args(), "Args(2):", Args(2)


def StringOrList(v):
    print "Type of", v, "is ", "a list" if (isinstance(v, list)) else "not a list"
#    
StringOrList(["a"])    
StringOrList("a")


# Create time tag and joint log name
from time import gmtime, strftime
time_tag = strftime("%Y_%m_%d__%H_%M_%S", gmtime())
print "Time tag:", time_tag 
print "Joint name: ", "_".join([time_tag] + Args()) 


print """
=== Substitutions ==="""

import string
def IsRecursiveSubstitution(substitutions):
    print substitutions
    for (k, s) in substitutions.iteritems():
        p = "${" + k + "}"
        if (p in s):
            return True
    return False
print IsRecursiveSubstitution({"p0": "( ${p1})", "p1": "0"})
print IsRecursiveSubstitution({"p0": "( ${p1})", "p1": " !!! ${p1} !!! "})


def IterativeSubstitution(pattern, substitutions):
    print substitutions
    resolved_string = None
    while(resolved_string != pattern):
        pattern = resolved_string or pattern
        try:
            template = string.Template(pattern)
            resolved_string = template.substitute(**substitutions)
        except KeyError as e:
            print "Missing pattern to substitute: ", e.args[0]
            # One option is to leave missing pattern as is
            substitutions[e.args[0]] = "${" + e.args[0] + "}"
            # or propagate exception furthure
        #print "  ", resolved_string
    return resolved_string

print IterativeSubstitution("Simple substitution: ${p0}", {"p0": "sub0"})
print IterativeSubstitution("Complex substitution: ${p0}", 
                            {"p0": "${p1} + ${p2}", "p1": "~${p2}", "p2": "sub0"})

def RunConsole(command, **substitutes):
    for (k, v) in substitutes.iteritems():
        print k, ": ",   v
    print ">", IterativeSubstitution(command, substitutes)
    
RunConsole("irun -f irun.f -l ${test_name}.log ${run_args} +undefined+${undefined_arg}", 
            test_name = "reset_test", 
            run_args = "+define+USE_PLL")


print """
=== Test call ==="""

def Test(name, count = None, run_args = None):
    pass
Test("fifo_test")                  
Test(name = "read_memory_model_test", run_args = "+define+CONNECT_MEMORY_MODEL")

import subprocess
def RunCommand(command):
    # Manage command logging and command output ...
    return subprocess.call(command, shell = True)
def RunCommandList(commands):
    return map(RunCommand, commands)
commands = ["ls -l", "sleep 1", "exit 1"]
#print "Running ", commands, "results in", RunCommandList(commands)
    

import multiprocessing
import multiprocessing.pool
import time

# By default processes created by multiprocessing.Pool 
# can not create other processes (this is required to implement timeout)
# because daemon property is True and can not be altered
class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def f(x):
    print "Started", x
    time.sleep(x)
    print "Finished", x
    return (x, x^2)

def RunTest(x):
    p = multiprocessing.Pool(1)                     # Using Pool (again) provides
    result = p.apply_async(func = f, args=(x,))   # convenient AsyncResult object
    try:
        return result.get(4)
    except multiprocessing.TimeoutError:
        p.terminate()
        print "Terminated", x      
    return None

def TestPoolExecution():                    
    pool = MyPool(processes=2)    
    result = pool.map(RunTest, [2, 1, 8, 3, 7])
    print result

if __name__ == '__main__':      # Module entry point should be protected 
                                # (it allows module to be safely imported 
                                # by new thread which calls a function)
    TestPoolExecution()
