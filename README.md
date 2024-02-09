# Python Package Template
Template of Python project wrapped as package that can be easily uploaded to PyPi

## Getting Started
To use this template click "Use this template" and create a new repository or open the template in a codespace [or use this template here](https://github.com/new?template_name=python-package-template&template_owner=mldxo)

## Usage - Linux
Create virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
After that you would adapt the code and continue when the project is ready to be published. Build the package using:
```
python setup.py sdist bdist_wheel
```
Test compiled package locally using:
```
pip install dist/package-xx.whl
```
Before publishing to PyPi create account and get API key.
Save API key in your session using:
```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=$actual_token
```
Publish the package to PyPi:
```
twine upload dist/*
```
