import json

from collection import Collection

class Transaction(object):

    def __init__(self):

        self.collection = None

    def load(self):

        # read the file
        with open("data/collections/default.mtgcollection", "r") as collection_file:
            collection_as_json = json.loads(collection_file.read())

        # get name
        collection_name = collection_as_json["name"]

        # get cards
        collection_cards = {}
        for name, quantity in collection_as_json["cards"].items():
            collection_cards[name] = quantity

        self.collection = Collection(name=collection_name, cards=collection_cards)

    def save(self):

        # serialise the data
        output_dict = {
            "name": self.collection.get_name(),
            "cards": self.collection.get_cards(),
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
