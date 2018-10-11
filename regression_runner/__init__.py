"""
The package is used to run tests and analyse run output.
"""

from regression_input import Substitute, Test, Group, Run, Args, Env
from action_templates import *

import logging

logging.basicConfig(
    level=logging.WARNING,
    format="[%(levelname)s] %(filename)s %(funcName)s():\n%(message)s"
)