# setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

with open("version", "r") as file:
    version = file.read()

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
