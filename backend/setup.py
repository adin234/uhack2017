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
    name='UHACK BACKEND',
    version='1.0',
    description='Uhack backend api',
    long_description=_long_description,
    url='https://github.com/adin234/uhack2017',

    # Author details
    author='BEE FREE',
    author_email='dev@beefree.com',

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
