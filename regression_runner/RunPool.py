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
import logging


class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


def RunCommands(commands, log_file_name = None):
    max_commands = 3
    logging.info("Run commands: {} {}".format(commands[0:max_commands], 
                    "" if len(commands) < max_commands else 
                    "(not all commands shown)"))
                    
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


class RunPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

    def __init__(self, processes):
        super(RunPool, self).__init__(processes)
        self.processes = processes
        self.next_process_id = 0
        self.running_result_objects = {}
        self.finished_result_objects = {}


    def WaitAnyProcessToFinish(self):
        pass

    def ExecuteCommands(self, commands, timeout, test_result):
        """
        Sends commands to pool if there are free workers
        If all workers are busy then wait for any to finish
        """
        func = self.RunCommandsWithTimeout
        args = (commands, timeout, test_result)
        
        if (len(self.running_result_objects) >= self.processes):
            self.WaitAnyProcessToFinish()
        
        r = self.apply_async(func = func, args = args)
        self.running_result_objects[self.next_process_id] = r
        self.next_process_id += 1
        
    

    @staticmethod
    def RunCommandsWithTimeout(commands, timeout, test_result):
        p = multiprocessing.Pool(1)
        r = p.apply_async(func = RunCommands, args=(commands, test_result.log_file_name))
        try:
            test_result.return_codes = r.get(timeout)
        except multiprocessing.TimeoutError:
            p.terminate()
            test_result.timeout = True

