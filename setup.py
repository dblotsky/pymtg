#! /usr/bin/python

import os

from distutils.core import setup

setup(
    name         = 'PyMTG',
    version      = '0.1',
    description  = 'Python Magic: The Gathering collection manager.',
    author       = 'Serghei Filippov, Dmitry Blotsky',
    author_email = 'saevon.kyomae@gmail.com, dmitry.blotsky@gmail.com',
    url          = 'https://github.com/dblotsky/pymtg',
    scripts      = ['pymtg/mtg.py'],
    packages     = ['pymtg', 'pymtg.data'],
    package_dir  = {'pymtg': 'pymtg'},
    package_data = {
        'pymtg': [
            'data/*.json',
            'data/*.pymtg-settings',
        ]
    },
)
