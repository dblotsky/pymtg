#! /usr/bin/python

from setuptools import setup

setup(
    name         = 'PyMTG',
    version      = '0.1',
    description  = 'Python Magic: The Gathering collection manager.',
    author       = 'Serghei Filippov, Dmitry Blotsky',
    author_email = 'saevon.kyomae@gmail.com, dmitry.blotsky@gmail.com',
    url          = 'https://github.com/dblotsky/pymtg',
    py_modules   = ['card', 'collection', 'deck', 'format_json', 'graph', 'library', 'transaction', 'mtg'],
    scripts      = ['mtg']
)