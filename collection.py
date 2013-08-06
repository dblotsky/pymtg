class Collection(object):
    """
    A Magic: The Gathering card collection.
    """

    def __init__(self, name=u"Unnamed Collection", cards=None):

        super(Collection, self).__init__()

        self.__name = name

        if cards is None:
            cards = {}
        self.__cards = cards

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):

        return_string = u"Cards in {name}:\n".format(name=self.get_name())

        if len(self.__cards) == 0:
            return_string += u"No cards."

        else:
            cards_as_strings = []

            # format the cards
            for card_name, card_quantity in self.__cards.items():
                cards_as_strings.append(u"    {name}: {quantity}".format(name=card_name, quantity=card_quantity))

            return_string += u"\n".join(cards_as_strings)

        return return_string

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

    def get_name(self):
        return self.__name

    def get_cards(self):
        return self.__cards
