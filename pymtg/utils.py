import json

def json_file_as_dict(file_name):

    with open(file_name, "r") as json_file:
        return json.load(json_file)

def json_dict_to_file(file_name, target_dict):

    with open(file_name, "w+") as json_file:
        json.dump(target_dict, json_file)
