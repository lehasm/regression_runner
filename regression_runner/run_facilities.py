"""
Functions and auxiliary classes to run commands 
in separate processes with timeout
"""


#
# Auxiliary classes to support multiprocessing
#

import multiprocessing
import multiprocessing.pool


class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


#
# Run commands
#

import subprocess
import logging

def RunCommands(commands, log_file = None):
    max_commands = 3
    logging.info("Run commands: {} {}".format(commands[0:max_commands], 
                    "" if len(commands) < max_commands else 
                    "(not all commands shown)"))
    return_codes = []
    for c in commands:
        logging.debug("Run command {}".format(c))
        return_codes.append(
            subprocess.call(c, stdout=log_file, stderr=log_file, shell=True))
    return return_codes


def RunCommandsWithTimeout(commands, timeout, test_result):
    p = multiprocessing.Pool(1)
    result = p.apply_async(func = RunCommands, args=(commands, test_result.log_file))
    try:
        test_result.return_codes = result.get(timeout)
    except multiprocessing.TimeoutError:
        p.terminate()
        test_result.timeout = True
    
    
    