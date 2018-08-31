
from RunDescriptionObject import RunDescriptionObject
from GroupObject import GroupObject

import logging

class RunObject(RunDescriptionObject):
    """ Class to manage regression run  """

    default_group_name = "default"

    def __init__(self):
        super(RunObject, self).__init__("RunObject")

        self.parallel_processes = 1          # parallel execution disabled by default
        self.parallel_groups_allowed = False
        self.groups = {}
        self.SelectGroup(self.default_group_name)

    def SelectGroup(self, name):
        self.selected_group = name
        if name not in self.groups:
            self.groups[self.selected_group] = GroupObject(self.selected_group)

    def AddTest(self, name):
        pass

    def Run(self):
        pass



