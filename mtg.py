#!/usr/bin/python

import argparse



def list_cards(args):
    print 'Indestructability: 1'
    print 'Fortuous Awesome: 3'

def add_card(args):
    print 'add card'
    print args


def parse_args():
    main_parser = argparse.ArgumentParser(
        description='TODO',
    )
    main_parser.subparsers = main_parser.add_subparsers()

    cards_parser = main_parser.subparsers.add_parser(
        'cards',
        help='Lists the cards you have',
    )
    cards_parser.set_defaults(func=list_cards)

    add_card_parser = main_parser.subparsers.add_parser(
        'add',
        help='Adds a new card',
    )
    add_card_parser.add_argument('-n', '--number', type=int, dest='num', default=1)
    add_card_parser.set_defaults(func=add_card)

    return main_parser.parse_args()




if __name__ == '__main__':
    args = parse_args()
    args.func(args)

