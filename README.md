# PyMTG

This is a command-line utility to manage a Magic: The Gathering card collection.

## Installing

To install, simply run the following (requires root privilege):

    make install

The `install` target forcefully (`-f` option) creates a symbolic link, `/usr/bin/mtg`, to the main pymtg executable, `mtg.py`. It also downloads a copy of the Magic: The Gathering card database. The download can also be carried out independently by running:

    make download

If permissions are a problem when executing, let `mtg.py` be executable by running:

    chmod +x mtg.py

## Running

After installing, simply run:

    mtg

Cards can be added via:

    mtg add <card_name>

## Data

For now, the data are in large JSON files, and are downloaded to the `data` directory. There are two data files: [AllSets.json][allsets] and [AllSets-x.json][allsets-x].

[allsets]:   http://mtgjson.com/json/AllSets.json
[allsets-x]: http://mtgjson.com/json/AllSets-x.json
