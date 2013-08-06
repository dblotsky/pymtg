import json

from card import Card

class Library(object):
    """
    The library of all Magic: The Gathering cards.
    """

    def __init__(self, cards):

        self.__cards = {}
        for card in cards:
            self.__cards[card.get_name()] = card

    def lookup(self, name):
        return self.__cards[name]

    def get_card_names(self):
        return self.__cards.keys()
