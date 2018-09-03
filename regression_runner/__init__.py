"""
The package is used to run tests and analyse run output.
"""

# To call unit tests:
# python -m unittest discover --start-directory tests --pattern *.py

from regression_input import Run, Test, Group
from action_templates import *

import logging

logging.basicConfig(
    level=logging.WARNING,
    format="[%(levelname)s] %(filename)s %(funcName)s():\n%(message)s"
)