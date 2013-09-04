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
    data_files = [
        (os.path.expanduser('~/.pymtg/collections'), ['pymtg/data/collections/sample.mtgcollection']),
        (os.path.expanduser('~/.pymtg/decks'), ['pymtg/data/decks/sample.mtgdeck']),
        (os.path.expanduser('~/.pymtg'), ['pymtg/data/preferences.pymtg-settings']),
    ]
)
