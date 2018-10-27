
import multiprocessing
import time

def WaitAndPrint(s, str):
    time.sleep(s)
    print(str)

def TestMultiprocessing():
    print "TestMultiprocessing"
    p = multiprocessing.Pool(2)
    result = p.apply_async(func = WaitAndPrint, args=(4, "0"))
    result = p.apply_async(func = WaitAndPrint, args=(1, "1"))
    result = p.apply_async(func = WaitAndPrint, args=(1, "2"))
    result = p.apply_async(func = WaitAndPrint, args=(1, "3"))
    # All apply_async returns immediately
    # Tasks for processes for execution are stored inside pool
    # and launched as worker are ready for new task
    print "applied"
    time.sleep(5)
    print "TestMultiprocessing done"

if __name__ == '__main__':      # Module entry point should be protected 
                                # (it allows module to be safely imported 
                                # by new thread which calls a function)
    TestMultiprocessing()