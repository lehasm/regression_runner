"""
Functions for describing test run and tuning it
"""

from RunObject import RunObject, R
from GroupObject import GroupObject
from TestObject import TestObject

import sys
import os


def Args(i = None):
    """
    Simplifies way to get command line arguments
    Reorganizes sys.argv: excludes its zero argument,
    numbers remaining arguments starting with zero.
    Returns argument with index passed,   
    returns reorganized array if called without i (Args())
    """
    if (i is None):
        return sys.argv[1:]
    elif (0 <= i < len(sys.argv)-1):
        return sys.argv[1 + i]
    else:    
        return ""


def Env(name):
    return os.getenv(name) or ""

def Substitute(**kwargs):
    R.UpdateRunContext(kwargs)


def Run(**kwargs):
    """ Updates RunObject global configuration and launches regression  """
    for (name, value) in kwargs.iteritems():
        getattr(R, name)        # check whether attribute with the name exists. Raise AttributeError otherwise
        setattr(R, name, value)
    R.Run()


def Group(name, **kwargs):
    g = GroupObject(name)
    g.UpdateRunContext(kwargs)
    R.AddGroup(g)


def Test(name, **kwargs):
    t = TestObject(name)
    t.UpdateRunContext(kwargs)
    R.AddTest(t)
