from graph import bar_graph

class Collection(object):
    """
    A Magic: The Gathering card collection.
    """

    def __init__(self, library, name, cards=None):

        self.__name    = name
        self.__library = library

        if cards is None:
            cards = {}
        self.__cards = cards

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):

        # get color graph
        graph_string = bar_graph(self.get_colour_distribution())

        # indent every line in the graph
        graph_string = "\n".join(map(lambda x: "    " + x, graph_string.split("\n")))

        # create the format string
        format_string = ""
        format_string += "\n"
        format_string += "Collection: {name}\n"
        format_string += "Card Count: {num}\n"
        format_string += "\n"
        format_string += "Card Colour Graph:\n"
        format_string += "{colours}\n"
        format_string += "\n"
        format_string += "Card List:\n"
        format_string += "{cards}"
        format_string += "\n"

        # format the output
        return format_string.format(
            name=self.get_name(),
            num=sum(self.__cards.values()),
            colours=graph_string,
            cards=self.get_card_list()
        )

    def add(self, card_name, quantity=1):

        if card_name in self.__cards:
            self.__cards[card_name] += quantity
        else:
            self.__cards[card_name] = quantity

    def remove(self, card_name, quantity=1, remove_all=False):

        if remove_all:
            self.__cards[card_name] = 0
        else:
            self.__cards[card_name] = max(self.__cards[card_name] - quantity, 0)

    def forget(self, card_name):
        self.__cards.pop(card_name, None)

    def get_colour_distribution(self):

        histogram = {}

        for card_name in self.get_card_names():

            colors = self.__library.lookup(card_name).get_colors()

            for color in colors:
                if color in histogram:
                    histogram[color] += self.count(card_name)
                else:
                    histogram[color] = self.count(card_name)

        return histogram

    def get_card_list(self):

        if self.count_cards() == 0:
            return u"    No cards."

        # get all cards as strings
        cards_as_strings = []
        for card_name, card_quantity in sorted(self.get_cards_with_quantities().items()):
            cards_as_strings.append(u"    {quantity:<3} {card}".format(quantity=card_quantity, card=self.get_library().lookup(card_name)))

        return u"\n".join(cards_as_strings)

    def count_cards(self):
        return len(self.get_card_names())

    def get_name(self):
        return self.__name

    def get_card_names(self):
        return self.__cards.keys()

    def get_cards_with_quantities(self):
        return self.__cards

    def count(self, card_name):
        return self.__cards[card_name]

    def get_library(self):
        return self.__library
