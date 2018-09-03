"""
Functions for describing test run and tuning it
"""

from RunObject import RunObject, R
from GroupObject import GroupObject
from TestObject import TestObject


def Substitute(**kwargs):
    R.UpdateRunContext(kwargs)


def Run(**kwargs):
    """ Updates RunObject global configuration and launches regression  """
    for (name, value) in kwargs.iteritems():
        getattr(R, name)        # check whether attribute with the name exists. Raise AttributeError otherwise
        setattr(R, name, value)
    R.Run()


def Group(name, **kwargs):
    R.AddGroup(name)


def Test(name, **kwargs):
    pass
