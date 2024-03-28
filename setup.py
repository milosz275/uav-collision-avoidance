"""Setup file for the uav-collision-avoidance"""

from setuptools import setup, find_packages
from uav_collision_avoidance.version import __version__ as version

with open("README.md", "r", encoding="utf-8") as file:
    description = file.read()

setup(
    name = "uav-collision-avoidance",
    version = version,
    packages = find_packages(),
    install_requires = [
        "pyside6"
    ],
    entry_points = {
        "console_scripts" : [
            "uav-collision-avoidance = uav_collision_avoidance:main",
        ],
    },
    long_description = description,
    long_description_content_type = "text/markdown",
)
