#! /usr/bin/python

import argparse
import difflib

from transaction import Transaction

# config
SIMILARITY      = 0.6
MAX_NUM_MATCHES = 100

def list_cards(args, context):
    print context.get_collection()

def present_card_choices(target, matches):

    if len(matches) == 0:
        return None

    elif len(matches) == 1:

        print u"Found matching card:", matches[0]

        if prompt_user(u"Is this the card you wanted?") is False:
            return None
        else:
            return matches[0]

    else:

        print u"Found more than one cards that match:"

        for i, card in enumerate(matches):
            print u"    [{i}]: {card}".format(i=(i + 1), card=card)

        print u"NOTE: only up to {limit} cards are displayed.".format(limit=MAX_NUM_MATCHES)

        while True:

            answer = raw_input(u"Please choose a card, or 'n' to reject all. [1 - {top}, n]: ".format(top=len(matches)))

            if answer == "n":
                return None

            try:
                return matches[int(answer) - 1]

            except (ValueError, KeyError):
                pass


        return None

def prompt_user(question):

    while True:

        answer = raw_input(question + u" [Y/n]: ")

        if answer == "Y":
            return True
        elif answer == "n":
            return False

def fuzzy_search(needle, haystack, no_input=False):

    matches = difflib.get_close_matches(needle, haystack, n=MAX_NUM_MATCHES, cutoff=SIMILARITY)

    # if exact match found, use it
    if needle in matches:
        return needle

    # if there was no exact match and if input is ignored, then return nothing
    if no_input:
        return None

    # prompt for inexact match
    chosen_name = present_card_choices(needle, matches)
    if chosen_name is not None:
        return chosen_name

    return None

def find_card(name, context, should_search_lib=True, no_input=False):

    # flag to say that a search needs to happen
    still_searching = True

    # first check collection
    if still_searching:

        chosen_name = fuzzy_search(name, context.get_collection().get_cards().keys(), no_input=no_input)

        if chosen_name is not None:
            still_searching = False

    # then check the library
    if still_searching and should_search_lib:

        if (not no_input) and prompt_user(u"Card not found in collection. Do you want to escalate the search to the MTG library?") is False:
            return

        chosen_name = fuzzy_search(name, context.get_card_library().keys(), no_input=no_input)

        if chosen_name is not None:
            still_searching = False

    if still_searching:
        return None

    return chosen_name

def add_card(args, context):

    card_quantity = args.num

    if args.force is False:
        card_name = find_card(name=args.title, context=context, should_search_lib=True, no_input=args.no_input)
    else:
        card_name = args.title

    if card_name is None:
        print u"Card not found."

    else:

        # add the card
        context.get_collection().add(card_name, card_quantity)

def remove_card(args, context):

    card_quantity = args.num

    if args.force is False:
        card_name = find_card(name=args.title, context=context, should_search_lib=False, no_input=args.no_input)
    else:
        card_name = args.title

    if card_name is None:
        print u"Card not found."

    else:

        # remove the card
        if args.force:
            context.get_collection().forget(card_name)
        else:
            context.get_collection().remove(card_name, card_quantity, remove_all=args.remove_all)

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

    remove_card_parser = main_parser.subparsers.add_parser(
        'remove',
        help='Removes cards from your collection',
    )
    remove_card_parser.add_argument('title')
    remove_card_parser.add_argument('-a', '--all', action='store_true', dest='remove_all', default=False)
    remove_card_parser.add_argument('-n', '--number', type=int, dest='num', default=1)
    remove_card_parser.add_argument('-f', '--force', action='store_true', dest='force', default=False)
    remove_card_parser.add_argument('--no-input', action='store_true', dest='no_input', default=False)
    remove_card_parser.set_defaults(func=remove_card)

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
