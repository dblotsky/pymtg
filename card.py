import json

class Card(object):
    """
    A Magic: The Gathering card.
    """

    def __init__(self, name, cost):

        self.name = name
        self.cost = cost

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost
