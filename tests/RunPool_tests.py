# To call form command line:
# python -m unittest tests.RunPool_tests

import unittest
import os, time

from regression_runner.RunPool import RunPool
from regression_runner.RunPool import RunCommands, RunCommandsWithTimeout
from regression_runner.ResultObject import ResultObject


class TestRun(unittest.TestCase):

    def setUp(self):
        self.processes = 2
        self.obj = RunPool(self.processes)
        self.result_object = ResultObject()
        self.immediate_commands = ["exit {}".format(i) for i in range(3)]

    def tearDown(self):
        pass

    def StartSomeImmediateCommands(self, count):
        for i in range(count):
            self.obj.StartCommandsExecution(self.immediate_commands, 10, self.result_object)

    def test_Init(self):
        self.assertEqual(self.obj.processes, self.processes)
        
        
    def test_StartCommandsExecution(self):
        count = 2
        for i in range(count):
            id = self.obj.StartCommandsExecution(self.immediate_commands, 10, self.result_object)
            self.assertEqual(id, i)
        self.assertEqual(len(self.obj.running_result_objects), count)
        self.assertEqual(len(self.obj.finished_result_objects), 0)

        self.obj.WaitFreeWorkers(2)
        self.obj.WaitFreeWorkers()
        
        self.assertEqual(len(self.obj.running_result_objects), 0)
        self.assertEqual(len(self.obj.finished_result_objects), count)
        
        
    def test_WaitAnyCommandsExecution(self):
        count = 3
        self.StartSomeImmediateCommands(count)
        ids = []
        for i in range(count):
            ids.append(self.obj.WaitAnyCommandsExecution())
        self.assertEqual(sorted(ids), range(count))
        self.assertEqual(self.obj.WaitAnyCommandsExecution(), False)
    
    
    def test_WaitCommandsExecution(self):
        count = 2
        self.StartSomeImmediateCommands(count)
        
        with self.assertRaises(AssertionError):
            self.obj.WaitCommandsExecution(count + 1)    
    
        for i in range(count):
            self.obj.WaitCommandsExecution(i)
        
        with self.assertRaises(AssertionError):
            self.obj.WaitCommandsExecution(0)    
    
    
    def test_Execution(self):
        id = self.obj.StartCommandsExecution(["sleep 1", "exit 2"],
                10, self.result_object)        
        self.assertTrue(id in self.obj.running_result_objects)
        self.obj.WaitCommandsExecution(id)
        self.assertTrue(id not in self.obj.finished_result_objects)
        self.assertEqual(self.result_object.return_codes, [0, 2])
        
        

    #@unittest.skip("skip while debugging")
    def test_RunCommands(self):
        return_codes = [0, 1, 255]
        commands = ["exit {}".format(r) for r in return_codes]
        self.assertEqual(RunCommands(commands, None), return_codes)

        temp_name = "test_RunCommands.log"
        test_string = "test"
        self.assertEqual(RunCommands(["echo " + test_string], temp_name), [0])
        with open(temp_name, 'r') as f:
            f_content = f.read()
            f.close()
            os.remove(temp_name)
            self.assertEqual(f_content, 
                "\n> echo {0}\n{0}\n".format(test_string))
            
    #@unittest.skip("skip while debugging")    
    def test_RunCommandsWithTimeout(self):
        test_result = ResultObject("test.log")
        timeout = 1
        return_codes = [0, 1, 255]
        commands = ["exit {}".format(r) for r in return_codes]
        RunCommandsWithTimeout(commands, timeout, test_result)
        test_result.RemoveLog()
        self.assertEqual(test_result.return_codes, return_codes)
        self.assertEqual(test_result.timeout, False)
        
        RunCommandsWithTimeout(["sleep {}".format(timeout + 1)], timeout, test_result)
        self.assertEqual(test_result.timeout, True)
        
