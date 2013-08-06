class Collection(object):
    """
    A Magic: The Gathering card collection.
    """

    def __init__(self, name="Unnamed Collection", cards=None):

        super(Collection, self).__init__()

        self.name = name

        if cards is None:
            cards = {}
        self.cards = cards

    def __str__(self):

        if len(self.cards) == 0:
            return "No cards."

        cards_as_strings = []

        # format the cards
        for card_name, card_quantity in self.cards.items():
            cards_as_strings.append("{name}: {quantity}".format(name=card_name, quantity=card_quantity))

        return "\n".join(cards_as_strings)

    def add(self, card_name, quantity=1):

        if card_name in self.cards:
            self.cards[card_name] += quantity
        else:
            self.cards[card_name] = quantity

    def get_name(self):
        return self.name

    def get_cards(self):
        return self.cards
