from graph import bar_graph

class Collection(object):
    """
    A Magic: The Gathering card collection.
    """

    def __init__(self, library, name=u"Unnamed Collection", cards=None):

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
        format_string += "Collection: {name}\n"
        format_string += "Card Count: {num}\n"
        format_string += "Colour Graph:\n"
        format_string += "{colours}\n"
        format_string += "Card List:\n"
        format_string += "{cards}"

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

        print u"added {0} of {1}".format(quantity, card_name)

    def remove(self, card_name, quantity=1, remove_all=False):

        if remove_all:
            self.__cards[card_name] = 0
        else:
            self.__cards[card_name] = max(self.__cards[card_name] - quantity, 0)

        print u"tried to remove {0} of {1}; now at {2}".format(quantity, card_name, self.__cards[card_name])

    def forget(self, card_name):
        self.__cards.pop(card_name, None)

    def get_colour_distribution(self):

        histogram = {}

        for card_name in self.get_cards():

            colors = self.__library.lookup(card_name).get_colors()

            for color in colors:
                if color in histogram:
                    histogram[color] += 1
                else:
                    histogram[color] = 1

        return histogram

    def get_card_list(self):

        if len(self.__cards) == 0:
            return u"    No cards."

        cards_as_strings = []

        # format the cards
        for card_name, card_quantity in self.__cards.items():
            cards_as_strings.append(u"    {name}: {quantity}".format(name=card_name, quantity=card_quantity))

        return u"\n".join(cards_as_strings)

    def get_name(self):
        return self.__name

    def get_cards(self):
        return self.__cards.keys()

    def get_cards_with_quantities(self):
        return self.__cards
