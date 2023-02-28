# Setup script for the `kitchen` package.
#
# Author: Oleksandr Liakhov <eleutherius69@gmail.com>
# Last Change: February 22, 2023

# Standard library modules.
import codecs
import os
import re

# De-facto standard solution for Python packaging.
from setuptools import setup, find_packages

# Find the directory where the source distribution was unpacked.
source_directory = os.path.dirname(os.path.abspath(__file__))

# Find the current version.
module = os.path.join(source_directory, 'src', '__init__.py')
for line in open(module):
    match = re.match(r'^__version__\s*=\s*["\']([^"\']+)["\']$', line)
    if match:
        version_string = match.group(1)
        break
else:
    raise Exception(f"Failed to extract version from {module}!")

# Fill in the long description (for the benefit of PyPI)
# with the contents of README.md (rendered by GitHub).
readme_file = os.path.join(source_directory, 'README.md')
with codecs.open(readme_file, 'r', 'utf-8') as handle:
    readme_text = handle.read()

setup(name='kitchen',
      version=version_string,
      description="ARMBSD kitchen",
      long_description=readme_text,
      url='https://github.com/armbsd/kitchen',
      author='Oleksandr Liakhov',
      author_email='eleutherius69@gmail.com',
      packages=find_packages(),
      entry_points=dict(console_scripts=[
        'kitchen = src.kitchen:main'
      ]),
      install_requires=[
        'click',
        'Jinja2'
      ],
      tests_require=[
        'ruff',
      ],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Systems Administration',
      ])

