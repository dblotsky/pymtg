import json

class Card(object):
    """
    A Magic: The Gathering card.
    """

    def __init__(self, name, colors, extra_data=None):

        self.__name   = name
        self.__colors = colors

        if extra_data is None:
            extra_data = {}
        self.__extra_data = extra_data

    def get_name(self):
        return self.__name

    def get_extra_data(self):
        return self.__extra_data

    def get_colors(self):
        return self.__colors

    def __unicode__(self):
        return "{name}".format(name=self.get_name())
