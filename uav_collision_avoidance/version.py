"""Contains the version of the package"""

import toml

def get_version():
    try:
        pyproject = toml.load("pyproject.toml")
        return pyproject["project"]["version"]
    except:
        return ""

__version__ = get_version()
