import json

class Card(object):
    """
    A Magic: The Gathering card.
    """

    def __init__(self, name, cost, extra_data=None):

        self.__name = name
        self.__cost = cost

        if extra_data is None:
            extra_data = {}
        self.__extra_data = extra_data

    def get_name(self):
        return self.__name

    def get_cost(self):
        return self.__cost
