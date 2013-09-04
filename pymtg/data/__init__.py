import os.path

from pymtg.utils import json_file_as_dict, json_dict_to_file

# directories
USER_DATA_DIR   = os.path.expanduser("~/.pymtg")
GLOBAL_DATA_DIR = os.path.dirname(__file__)
COLLECTION_DIR  = os.path.join(USER_DATA_DIR, "collections")

# files
LIBRARY_FILE          = os.path.join(GLOBAL_DATA_DIR, "AllSets.json")
SETTINGS_FILE         = os.path.join(USER_DATA_DIR, "preferences.pymtg-settings")
DEFAULT_SETTINGS_FILE = os.path.join(GLOBAL_DATA_DIR, "default-settings.json")

# setting names
SETTING_COLLECTION = "current_collection"

# extensions
COLLECTION_EXTENSION = ".mtgcollection"

# setting dict
__settings = None

def get_setting(setting_name):

    global __settings

    if __settings is None:
        load_settings()

    return __settings[setting_name]

def set_setting(setting_name, value):

    global __settings

    if __settings is None:
        load_settings()

    if (setting_name not in __settings) or (__settings[setting_name] != value):
        __settings[setting_name] = value
        save_settings()

def load_settings():

    global __settings

    # re-create the settings file if it doesn't exist
    if not os.path.exists(SETTINGS_FILE):
        defaults = json_file_as_dict(DEFAULT_SETTINGS_FILE)
        json_dict_to_file(SETTINGS_FILE, defaults)

    # load the settings
    __settings = json_file_as_dict(SETTINGS_FILE)

def save_settings():

    global __settings

    json_dict_to_file(SETTINGS_FILE, __settings)
