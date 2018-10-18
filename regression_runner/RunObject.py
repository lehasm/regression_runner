
from RunDescriptionObject import RunDescriptionObject
from GroupObject import GroupObject
from TestResultObject import TestResultObject
from PrintObject import PrintObject
from run_facilities import *


import logging
from time import gmtime, strftime

class RunObject(RunDescriptionObject):
    """ Class to manage regression run  """

    _default_group_name = "_default"

    def __init__(self, name):
        super(RunObject, self).__init__(name)

        self.trail_run = False              # do not actually call run functions
        self.parallel_processes = 1         # parallel execution disabled by default
        self.parallel_groups_allowed = False
        self.groups = {}
        self.AddGroup(GroupObject(self._default_group_name))
        self.AddDefaultSubstitutions()

    def AddDefaultSubstitutions(self):
        self.substitutions["time_tag"] = strftime("%Y_%m_%d__%H_%M_%S", gmtime())
        self.substitutions["log_path"] = "./logs/${time_tag}"


    def AddGroup(self, g):
        if (g.name in self.groups):
            raise KeyError("Group name {} is already used. Names must be unique.".format(test.name))
        self.groups[g.name] = g
        self.active_group_name = g.name


    def AddTest(self, t, group_name = None):
        self.groups[group_name or self.active_group_name].AddTest(t)


    def Run(self, **kwargs):
        self.UpdateRunContext(kwargs)
        self.printer = PrintObject()
        self.printer.PrintSessionHeader(self)        
        self.InitFlatSubstitutions()
     
    

R = RunObject("RunObject")
