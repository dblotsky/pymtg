class Collection(object):
    """
    A Magic: The Gathering card collection.
    """

    def __init__(self, owner_name="Unnamed Collection", cards=None):

        super(Collection, self).__init__()

        self.owner_name = owner_name

        if cards is None:
            self.cards = {}

    def __str__(self):

        result_string = ""

        for card_name, card_quantity in cards.items:
            result_string += "{name}: {quantity}\n".format(name=card_name, quantity=card_quantity)

    def add(self, card, quantity=1):

        card_name = card.name

        if card_name in cards:
            self.cards[card_name] += quantity
        else:
            self.cards[card_name] = quantity
