# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

setup(
    name = "python-package-template",
    version = "0.1",
    packages = find_packages(),
    install_requires = [], # insert dependencies
    entry_points = {
        "console_scripts" : [
            "python-package-template = python_package_template:main",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
