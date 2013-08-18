import os.path

from pymtg.utils import json_file_as_dict

# directories
DATA_DIR       = os.path.dirname(__file__)
COLLECTION_DIR = os.path.join(DATA_DIR, "collections")

# files
LIBRARY_FILE  = os.path.join(DATA_DIR, "AllSets.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "preferences.pymtg-settings")

# setting dict
__settings = None

def get_setting(setting_name):

    global __settings

    if __settings is None:
        load_settings()

def load_settings():

    global __settings

    __settings = json_file_as_dict(SETTINGS_FILE)

