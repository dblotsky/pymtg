#! /usr/bin/python

import argparse
import difflib

from transaction import Transaction

def list_cards(args, context):
    print context.get_collection()

def present_card_choices(target, matches):

    if len(matches) == 1:

        print "Found matching card:", matches[0]

        if prompt_user("Is this the card you wanted?") is False:
            return None
        else:
            return matches[0]

    else:

        print "Found more than one cards that match:"

        for i, card in enumerate(matches):
            print "    [{i}]: {card}".format(i=(i + 1), card=card)

        while True:

            answer = raw_input("Please choose a card, or 'n' to reject all. [1 - {top}, n]: ".format(top=len(matches)))

            if answer == "n":
                return None

            try:
                return matches[int(answer) - 1]

            except (ValueError, KeyError):
                pass


        return None

def prompt_user(question):

    while True:

        answer = raw_input(question + " [Y/n]: ")

        if answer == "Y":
            return True
        elif answer == "n":
            return False

def add_card(args, context):

    # get parameters
    card_name     = args.title
    card_quantity = args.num

    # get collection
    collection = context.get_collection()

    # flag to say that a search needs to happen
    still_searching = True

    # don't search if the card is already in the collection
    if card_name in collection.get_cards():

        chosen_card_name = card_name
        still_searching  = False

    # first check collection
    if still_searching:

        matching_cards_in_collection = difflib.get_close_matches(card_name, collection.get_cards().keys())
        chosen_card_name             = present_card_choices(card_name, matching_cards_in_collection)

        if chosen_card_name is not None:
            still_searching = False

    # then check the library
    if still_searching:

        if prompt_user("Do you want to escalate the search to the MTG library?") is False:
            return

        # check card library
        card_library              = context.get_card_library()
        matching_cards_in_library = difflib.get_close_matches(card_name, card_library.keys())
        chosen_card_name          = present_card_choices(card_name, matching_cards_in_library)

        if chosen_card_name is not None:
            still_searching = False

    if still_searching:
        print "Card not found."
        return

    # add the card
    collection.add(chosen_card_name, card_quantity)

def parse_args():
    main_parser = argparse.ArgumentParser(
        usage='mtg [options]',
        description='TODO Description here',
    )
    main_parser.subparsers = main_parser.add_subparsers(
        title='commands',
    )

    help_parser = main_parser.subparsers.add_parser(
        'help',
        help='Show this help message',
    )
    help_parser.set_defaults(func=lambda args: main_parser.print_help())

    cards_parser = main_parser.subparsers.add_parser(
        'cards',
        help='Lists the cards you have',
    )
    cards_parser.set_defaults(func=list_cards)

    add_card_parser = main_parser.subparsers.add_parser(
        'add',
        help='Adds a new card',
    )
    add_card_parser.add_argument('title')
    add_card_parser.add_argument('-n', '--number', type=int, dest='num', default=1)
    add_card_parser.add_argument('-f', '--force', action='store_true', dest='force', default=False)
    add_card_parser.add_argument('--no-input', action='store_true', dest='no_input', default=False)
    add_card_parser.set_defaults(func=add_card)

    return main_parser.parse_args()


def main():
    # parse the args and find which command to run
    args = parse_args()

    # get the local data
    with Transaction() as context:

        # run the command
        args.func(args, context)

if __name__ == '__main__':
    main()
