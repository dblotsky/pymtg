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

            self.__card_library = Library("data/AllSets.json")
            self.__card_library.load()

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

        self.__collection = Collection(library=self.get_card_library(), name=collection_name, cards=collection_cards)

    def save(self):

        # serialise the data
        output_dict = {
            "name": self.__collection.get_name(),
            "cards": self.__collection.get_cards_with_quantities(),
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
