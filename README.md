# PyMTG

This is a command-line utility to manage a Magic: The Gathering card collection. It currently only has minimal functionality: creating card collections, switching among them, adding and removing cards to/from them, and viewing the cards in them.

## Installing

To install, simply run the following (might require `sudo`):

    make install

The installation downloads a copy of the Magic: The Gathering card database, and then installs the Python package using setuptools. The data download can also be carried out independently by running:

    make download

## Running

After installing, simply run:

    mtg.py

Help and command syntax can be viewed by running:

    mtg.py help

## Data

For now, the data are in large JSON files, and are downloaded to the `data` directory. There are two data files: [AllSets.json][allsets] and [AllSets-x.json][allsets-x].

[allsets]:   http://mtgjson.com/json/AllSets.json
[allsets-x]: http://mtgjson.com/json/AllSets-x.json
