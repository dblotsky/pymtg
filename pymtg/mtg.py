#! /usr/bin/python

import argparse
import difflib
import os
import sys

from subprocess import call
from pymtg.collection import Collection
from pymtg.transaction import Transaction
from pymtg.data import COLLECTION_SETTING, COLLECTION_DIR, COLLECTION_EXTENSION, get_setting, set_setting, setting_exists, create_data_dirs

# config
SIMILARITY      = 0.6
MAX_NUM_MATCHES = 100

PROGRAM_DESCRIPTION = """
This program is a command-line tool to manage Magic: The Gathering card collections and decks.
It can keep track of several collections and supports adding and removing cards.
"""

def list_cards(args, context):

    collection = context.get_collection()

    if collection is None:
        print "No collection selected. Select one using the 'switch' command."

    else:
        print collection

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

        answer = raw_input(question + u" [y/n]: ").lower()

        if answer == "y":
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

        chosen_name = fuzzy_search(name, context.get_collection().get_card_names(), no_input=no_input)

        if chosen_name is not None:
            still_searching = False

    # then check the library
    if still_searching and should_search_lib:

        if (not no_input) and prompt_user(u"Card not found in collection. Do you want to escalate the search to the MTG library?") is False:
            return

        chosen_name = fuzzy_search(name, context.get_card_library().get_card_names(), no_input=no_input)

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

def add_collection(args, context):

    new_collection_title = args.new_collection_name
    new_collection_file  = os.path.join(COLLECTION_DIR, (new_collection_title + COLLECTION_EXTENSION))

    # bail if the collection already exists
    try:
        with open(new_collection_file, "r") as f:
            print "Collection already exists."
        return

    # if we couldn't open collection file, it doesn't exist
    except IOError:
        pass

    # create the new collection file
    call(["touch", new_collection_file])

    # create the collection itself
    new_collection = Collection(None, new_collection_title)
    context.set_collection(new_collection)

    # make the collection default if there is no default
    if not setting_exists(COLLECTION_SETTING):
        set_setting(COLLECTION_SETTING, new_collection_title)

def get_all_collection_names():

    files_in_collection_dir = os.listdir(COLLECTION_DIR)
    collection_files_in_dir = filter(lambda x: (COLLECTION_EXTENSION in x), files_in_collection_dir)
    collection_names_only   = map(lambda x: x.replace(COLLECTION_EXTENSION, ""), collection_files_in_dir)

    return collection_names_only

def switch_collection(args, context):

    new_collection_name  = args.new_collection_name
    all_collection_names = get_all_collection_names()

    if new_collection_name not in all_collection_names:
        print "No such collection."
        return

    set_setting(COLLECTION_SETTING, new_collection_name)

def list_collections(args, context):

    all_collection_names = get_all_collection_names()

    if len(all_collection_names) == 0:
        print "No collections."
        return

    print "Available collections:"

    for collection_name in all_collection_names:
        print "   " + collection_name

def parse_args():

    # main
    main_parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION, add_help=False)
    subparsers = main_parser.add_subparsers()

    # help
    help_parser = subparsers.add_parser('help', help='Show this help message')
    help_parser.set_defaults(func=lambda args, context: main_parser.print_help())

    # cards
    cards_parser = subparsers.add_parser('cards', help='Lists the cards you have')
    cards_parser.set_defaults(func=list_cards)

    # status
    status_parser = subparsers.add_parser('status', help="Synonym for 'mtg cards'")
    status_parser.set_defaults(func=list_cards)

    # list
    list_parser = subparsers.add_parser('list', help="List all available collections")
    list_parser.set_defaults(func=list_collections)

    # create-collection
    init_parser = subparsers.add_parser('init', help="Creates a collection")
    init_parser.add_argument('new_collection_name', metavar='collection_name')
    init_parser.set_defaults(func=add_collection)

    # switch
    switch_parser = subparsers.add_parser('switch', help="Switches collections")
    switch_parser.add_argument('new_collection_name', metavar='collection_name')
    switch_parser.set_defaults(func=switch_collection)

    # add
    add_card_parser = subparsers.add_parser('add', help='Adds cards to the current collection')
    add_card_parser.add_argument('title', metavar='card_name')
    add_card_parser.add_argument('-n', '--number',   type=int,            dest='num',      default=1,     help="How many cards to add (Default: 1)")
    add_card_parser.add_argument('-f', '--force',    action='store_true', dest='force',    default=False, help="Add the card, even if we don't find it in the library")
    add_card_parser.add_argument('-q', '--no-input', action='store_true', dest='no_input', default=False, help="Add the card, only if we find an exact match, never prompting the user")
    add_card_parser.set_defaults(func=add_card)

    # remove
    remove_card_parser = subparsers.add_parser('remove', help='Removes cards from the current collection',)
    remove_card_parser.add_argument('title', metavar='card_name')
    remove_card_parser.add_argument('-a', '--all',               action='store_true', dest='remove_all', default=False, help="Remove all copies of the card")
    remove_card_parser.add_argument('-n', '--number',            type=int,            dest='num',        default=1,     help="How many cards to remove (Default: 1)")
    remove_card_parser.add_argument('-f', '--force', '--forget', action='store_true', dest='force',      default=False, help="Remove the card from the collection, forgetting it entirely")
    remove_card_parser.add_argument('-q', '--no-input',          action='store_true', dest='no_input',   default=False, help="Remove some copies of the card, only if we find an exact match, never prompting the user")
    remove_card_parser.set_defaults(func=remove_card)

    return main_parser.parse_args()


def main():

    # parse the args and find which command to run
    args = parse_args()

    # make sure that the data directories exist
    create_data_dirs()

    # get the local data
    with Transaction() as context:

        # run the command
        args.func(args, context)

if __name__ == '__main__':
    main()
