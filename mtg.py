#!/usr/bin/python

import argparse

from transaction import Transaction

def list_cards(args, context):
    print context.collection

def add_card(args, context):
    context.collection.add("Indesctuctibility", args.num)

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
