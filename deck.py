class Deck(object):
    """A deck of cards."""

    def __init__(self, name="Unnamed Deck", cards=[]):

        super(Deck, self).__init__()

        self.name  = name
        self.cards = cards
