import json

class Card(object):
    """
    A Magic: The Gathering card.
    """

    def __init__(self, json_data):
        self.json_data = json_data

    def __getattr__(self, attr_name):
        return self.json_data[attr_name]

    def __setattr__(self, attr_name, value):
        return self.json_data[attr_name] = value
