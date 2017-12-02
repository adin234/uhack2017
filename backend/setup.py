"""
Setup module for high level dependencies
of python dependencies
"""

import os

from codecs import open
from setuptools import setup

_cwd = os.path.abspath(os.path.dirname(__file__))

# Long description from README
# Use utf-8 for uniform encoding
with open(os.path.join(_cwd, 'README.md'), encoding='utf-8') as f:
    _long_description = f.read()

setup(
    name='Hacarus Backend API V2',
    version='2.0',
    description='New backend API for mobile v2.',
    long_description=_long_description,
    url='https://github.com/hacarus/hacarus-api-v2',

    # Author details
    author='Hacarus',
    author_email='dev@hacarus.com',

    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sqlalchemy',
        'pymysql',
        'flask_sqlalchemy',
        'requests',
        'uwsgi',
        'flask-cors',
        'Flask-Mail',
        'flask-login',
        'Flask-Testing',
        'Flask',
        'boto3',
        'colour-runner'
    ]
)
