import os
import sys

sys.path.append(os.path.abspath('../../../uav-collision-avoidance'))


project = 'uav-collision-avoidance'
copyright = '© 2024 Miłosz Maculewicz. All rights reserved.'
author = 'Miłosz Maculewicz'
release = '1.0.0'

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '*assets.rst',
    '*migrations*.rst',
]

html_theme = 'bizstyle'
html_static_path = ['_static']

# project = 'uav-collision-avoidance'
# copyright = '2024, Miłosz Maculewicz'
# author = 'Miłosz Maculewicz'
# release = '1.0.0'

# extensions = []

# templates_path = ['_templates']
# exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# html_theme = 'alabaster'
# html_static_path = ['_static']
