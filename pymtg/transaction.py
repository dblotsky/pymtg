import json
import sys
import os.path

from pymtg.collection import Collection
from pymtg.card import Card
from pymtg.library import Library
from pymtg.utils import json_file_as_dict
from pymtg.data import get_setting, LIBRARY_FILE, COLLECTION_DIR, SETTING_COLLECTION, COLLECTION_EXTENSION

class Transaction(object):

    def __init__(self):

        self.__collection   = None
        self.__card_library = None

    def get_card_library(self):

        if self.__card_library is None:

            # read the lbirary
            with open(LIBRARY_FILE) as library_file:
                library_json = json.loads(library_file.read())

            # retrieve the card data
            cards_as_json = []
            for card_set in library_json.values():
                cards_as_json.extend(card_set[u"cards"])

            # create the cards
            cards = []
            for card_data in cards_as_json:

                card_name = card_data[u"name"]

                # check for color of cards; some have no color
                if "colors" in card_data:
                    card_colors = card_data[u"colors"]
                else:
                    card_colors = []

                cards.append(Card(card_name, card_colors, card_data))

            self.__card_library = Library(cards)

        return self.__card_library

    def get_collection(self):

        if self.__collection is None:

            self.load()

        return self.__collection

    def set_collection(self, collection):

        if self.__collection is not None:
            self.save()

        self.__collection = collection

    def load(self):

        # read the collection
        collection_file_name     = get_setting(SETTING_COLLECTION) + COLLECTION_EXTENSION
        collection_file_location = os.path.join(COLLECTION_DIR, collection_file_name)
        collection_as_json       = json_file_as_dict(collection_file_location)

        # get name
        collection_name = collection_as_json["name"]

        # get cards
        collection_cards = {}
        for name, quantity in collection_as_json["cards"].items():
            collection_cards[name] = quantity

        self.__collection = Collection(library=self.get_card_library(), name=collection_name, cards=collection_cards)

    def save(self):

        # do nothing if there is no collection to save
        if self.__collection is None:
            return

        # serialise the data
        output_dict = {
            "name": self.__collection.get_name(),
            "cards": self.__collection.get_cards_with_quantities(),
        }
        collection_as_json = json.dumps(output_dict, indent=4)

        # output the data
        with open(os.path.join(COLLECTION_DIR, (get_setting(SETTING_COLLECTION) + COLLECTION_EXTENSION)), "w") as collection_file:
            collection_file.write(collection_as_json)

    def reset(self):
        self.__collection = None
        self.__card_library = None

    # methods for use with the "with" statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()
