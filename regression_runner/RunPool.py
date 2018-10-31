"""
Main class and auxiliary classes to run commands 
in separate processes with timeout
"""

"""
Перебор команд.

Вызвать функцию для выполнения команд
Если нет свободных параллельных процессов, то ждать, 
когда какой-нибудь освободится.
Если есть свободные, то запустить асинхронное выполнение с таймаутом.

Для не пересечения групп иметь возможность ожидать, когда завершаться все выполняемые процессы.

Все начальные команды группы должны завершиться до запуск тестов из группы.

Как возвращать результаты выполнения команд?
Для задачи нужно задавать номер и возвращать по номеру
"""

import multiprocessing
import multiprocessing.pool
import subprocess
import time
import logging

from regression_runner.ResultObject import ResultObject


class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


def RunCommands(commands, log_file_name = None):
    log_file = open(log_file_name, "a") if log_file_name else None
    command_string = "\n> {}\n"
    return_codes = []
    for c in commands:
        logging.debug("Run command {}".format(c))
        if log_file:
            log_file.write(command_string.format(c))
            log_file.flush()
        return_codes.append(
            subprocess.call(c, 
                stdout=log_file, stderr=log_file, 
                shell=True))
    if log_file:
        log_file.close()
    return return_codes


def RunCommandsWithTimeout(commands, timeout, log_file_name = None):
    max_commands = 3
    logging.info("Run commands (timeout = {}): {} {}".format(
                timeout, commands[0:max_commands], 
                    "" if len(commands) < max_commands else 
                    "(not all commands shown)"))

    test_result = ResultObject()
    p = multiprocessing.Pool(1)
    r = p.apply_async(func = RunCommands, args=(commands, log_file_name))
    try:
        test_result.return_codes = r.get(timeout)
    except multiprocessing.TimeoutError:
        p.terminate()
        test_result.timeout = True
    return test_result


class RunPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

    def __init__(self, processes):
        super(RunPool, self).__init__(processes)
        self.processes = processes
        self.last_process_id = -1
        self.running_processes = {}
        self.finished_results = {}
        self.traverse_interval = 1

    def TerminateAll(self):
        self.terminate()
        self.join()

    def TraverseResultObjects(self):
        """
        Iterates over result objects to find finished processes
        Moves these result objects to finished processes array
        """
        actual_running_processes = {}
        for (id, async_result) in self.running_processes.iteritems():
            if async_result.ready():
                self.finished_results[id] = async_result.get()
            else:
                actual_running_processes[id] = async_result
        self.running_processes = actual_running_processes


    def WaitFreeWorkers(self, free_count = 1):
        assert (0 <= free_count <= self.processes)
        while True:
            self.TraverseResultObjects()
            if (len(self.running_processes) <= 
                self.processes - free_count):
                break
            else:
                time.sleep(self.traverse_interval)
                
        
    def StartCommandsExecution(self, commands, timeout, log_file = None):
        """
        Sends commands to pool if there are free workers
        If all workers are busy then wait for any to finish
        """
        self.last_process_id += 1
        func = RunCommandsWithTimeout
        args = (commands, timeout, log_file)
        self.WaitFreeWorkers()
        
        async_result = self.apply_async(func = func, args = args)
        self.running_processes[self.last_process_id] = async_result
        
        return self.last_process_id
    
    
    def GetAnyResult(self):
        """
        Returns any finished process id and 
        object with result description
        or False if there is nothing to return or wait
        """
        if (len(self.finished_results) == 0 and
            len(self.running_processes) == 0):
                return (False, False)
        
        while True:
            self.TraverseResultObjects()
            if (len(self.finished_results) > 0):
                (id, r) = self.finished_results.popitem()
                return (id, r)
            else:
                time.sleep(self.traverse_interval)            

                    
    def GetResult(self, id):
        """
        Returns result object when the process 
        with given id has finished        
        If id is unknown to the class then rises exception
        """        
        assert(id in self.finished_results or
               id in self.running_processes)
        if (id in self.running_processes):
            self.running_processes[id].wait()
            self.TraverseResultObjects()
        r = self.finished_results[id]
        del self.finished_results[id]
        return r
    
    
    def WaitAllCommandsExecution(self):
        self.WaitFreeWorkers(self.processes)
