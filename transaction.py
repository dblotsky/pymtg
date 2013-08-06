import json

from collection import Collection
from card import Card

class Transaction(object):

    def __init__(self):

        self.__collection = None
        self.__card_library  = None

    def get_card_library(self):

        if self.__card_library is None:

            with open("data/AllSets.json") as library_file:
                library_json = json.loads(library_file.read())

            # retrieve just the cards
            cards = []
            for card_set in library_json.values():
                cards.extend(card_set["cards"])

            # map the cards to themselves
            self.__card_library = {}
            for card in cards:

                card_name = card["name"]
                self.__card_library[card_name] = Card(card_name, card)

        return self.__card_library

    def get_collection(self):
        return self.__collection

    def load(self):

        # read the files
        with open("data/collections/default.mtgcollection", "r") as collection_file:
            collection_as_json = json.loads(collection_file.read())

        # get name
        collection_name = collection_as_json["name"]

        # get cards
        collection_cards = {}
        for name, quantity in collection_as_json["cards"].items():
            collection_cards[name] = quantity

        self.__collection = Collection(name=collection_name, cards=collection_cards)

    def save(self):

        # serialise the data
        output_dict = {
            "name": self.__collection.get_name(),
            "cards": self.__collection.get_cards(),
        }
        collection_as_json = json.dumps(output_dict, indent=4)

        # output the data
        with open("data/collections/default.mtgcollection", "w") as collection_file:
            collection_file.write(collection_as_json)

    # methods for use with the "with" statement
    def __enter__(self):
        self.load()
        return self

    def __exit__(self, type, value, traceback):
        self.save()
