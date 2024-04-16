"""Contains the version of the package"""

import toml

def get_version():
    pyproject = toml.load("pyproject.toml")
    return pyproject['project']['version']

__version__ = get_version()
