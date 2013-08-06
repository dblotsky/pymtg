import json

from collection import Collection
from card import Card
from library import Library

class Transaction(object):

    def __init__(self):

        self.__collection   = None
        self.__card_library = None

    def get_card_library(self):

        if self.__card_library is None:

            # read the lbirary
            with open("data/AllSets.json") as library_file:
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
        with open("data/collections/default.mtgcollection", "r") as collection_file:
            collection_as_json = json.loads(collection_file.read())

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
        with open("data/collections/default.mtgcollection", "w") as collection_file:
            collection_file.write(collection_as_json)

    def reset(self):
        self.__collection = None
        self.__card_library = None

    # methods for use with the "with" statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()
