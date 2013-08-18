#! /usr/bin/python

import sys
import json
import argparse

def main():

    # set up argument parser
    parser = argparse.ArgumentParser(description="Format a single-line JSON file into a more human-readable format.")
    parser.add_argument("file", help="the file to format")

    # parse arguments
    args = parser.parse_args()

    # retrieve arguments
    data_file_name = args.file

    # process the file
    with open(data_file_name, "r+") as json_file:

        # read and format the data
        unformatted_data = json_file.read()
        data_as_json     = json.loads(unformatted_data)
        formatted_data   = json.dumps(data_as_json, indent=4, sort_keys=True)

        # rewind the file
        json_file.seek(0)

        # rewrite it formatted
        json_file.write(formatted_data)

if __name__ == "__main__":
    main()
