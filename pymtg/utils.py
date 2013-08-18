import json

def json_file_as_dict(file_name):

    with open(file_name, "r") as json_file:
        return json.load(json_file)


def json_dict_to_file(file_name, obj):
    with open(file_name, "r") as json_file:
        return json.dump(obj, json_file)

