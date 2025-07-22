# -*- coding: utf-8 -*-

# Prints the usage for each public dataset
#
# Author: Fernando Rios

import sys
import requests
import simplejson as json
from datetime import datetime
from os import environ
from trello import TrelloClient

sys.path.insert(0, 'lib/')
import functions as f


tc = None

def run(args):
    # Optionally writes a CSV report to file and returns a json array of objects with the data that was written.

    print('Getting curator stats from Trello')
    curators = []

    tc = TrelloClient(api_key=environ['API_TRELLO_KEY'], api_secret=environ['API_TRELLO_TOKEN'])
    
    try:
        board = tc.get_board(environ['TRELLO_BOARD_ID'])
        published_list = board.get_list(environ['TRELLO_PUBLISHEDLIST_ID'])
        cards = published_list.list_cards()
        for card in cards:
            print(card.name)
            for field in card.custom_fields:
                print(f'    {field.name}: {field.value}')
    except Exception as e:
        print(f'Error getting board info: {e}')

    outfile = None
    if args.outfile:
        outfile = f.get_report_outfile(args.outfile, 'curators')
        outfile.write(
            f'id,total_items,total_time ({args.units}),'
            + f'easy_items,easy_time ({args.units}),med_items,med_time ({args.units}),hard_items,hard_time ({args.units}),'
            + f'3M_items,3M_time ({args.units}),6M_items,6M_time ({args.units}),'
            + f'1Y_items,1Y_time ({args.units}),2Y_items,2Y_time ({args.units}),'
            + f'3M_easy_items,3M_easy_time ({args.units}),6M_easy_items,6M_easy_time ({args.units}),'
            + f'1Y_easy_items,1Y_easy_time ({args.units}),2Y_easy_items,2Y_easy_time ({args.units}),'
            + f'3M_med_items,3M_med_time ({args.units}),6M_med_items,6M_med_time ({args.units}),'
            + f'1Y_med_items,1Y_med_time ({args.units}),2Y_med_items,2Y_med_time ({args.units}),'
            + f'3M_hard_items,3M_hard_time ({args.units}),6M_hard_items,6M_hard_time ({args.units})'
            + f'1Y_hard_items,1Y_hard_time ({args.units}),2Y_hard_items,2Y_hard_time ({args.units})\n')
    else:
        print(f'id\t,total_items\t,total_time ({args.units})')

    # for article in articles:
        # if outfile:
            # s = '{0},{1},{2},{3},{4},{11},{5},{6},{7},{8},{9},{10},{12}'
        # else:
            # s = '{0}\t,{1}\t,{2}\t,{3}\t,{4}\t,{5}'

        # s = s.format(article['id'], article['version'], article['totalfilesize'],
                     # '"' + article['title'].replace('"', '""') + '"',
                     # article['type'],
                     # article['published_date'], article['modified_date'], article['embargo_date'], article['embargo_type'],
                     # article['embargo_options_type'], article['is_embargoed'], article['is_public'], article['report_date'])

        # if outfile:
            # outfile.write(s + '\n')
        # elif not args.sync_to_dashboard:
            # print(s)

    #print(f'Totals (hours):\t\t{total_usage}')
    #print(f'Totals ({args.units}):\t\t{f.format_bytes(total_usage, args.units)}')

    if outfile:
        outfile.close()

    return curators
