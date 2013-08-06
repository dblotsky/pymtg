import json

from card import Card

class Library(object):
    """
    The library of all Magic: The Gathering cards.
    """

    def __init__(self, file_name):

        self.__file_name = file_name

    def load(self):

        with open(self.__file_name) as library_file:
            library_json = json.loads(library_file.read())

        # retrieve just the cards
        cards_as_json = []
        for card_set in library_json.values():
            cards_as_json.extend(card_set[u"cards"])

        # map the card names to the cards
        self.__cards = {}
        for card_data in cards_as_json:

            card_name = card_data[u"name"]

            # check for color of cards; some have no color
            if "colors" in card_data:
                card_colors = card_data[u"colors"]
            else:
                card_colors = []

            self.__cards[card_name] = Card(card_name, card_colors, card_data)

    def lookup(self, name):
        return self.__cards[name]

    def get_cards(self):
        return self.__cards.keys()
