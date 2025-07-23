# -*- coding: utf-8 -*-

# Prints the usage for each public dataset
#
# Author: Fernando Rios

import sys
import traceback
import requests
import simplejson as json
from ast import literal_eval
from datetime import datetime
from os import environ
from trello import TrelloClient

sys.path.insert(0, 'lib/')
import functions as f


tc = None

def run(args):
    # Optionally writes a CSV report to file and returns a json array of objects with the data that was written.

    print('Getting curator stats from Trello')
    curators = {}

    tc = TrelloClient(api_key=environ['API_TRELLO_KEY'], api_secret=environ['API_TRELLO_TOKEN'])
    
    try:
        board = tc.get_board(environ['TRELLO_BOARD_ID'])
        boardmembers = board.all_members()
        published_list = board.get_list(environ['TRELLO_PUBLISHEDLIST_ID'])
        cards = published_list.list_cards()
        for card in cards:
            print(card.name)
            for field in card.custom_fields:
                print(f'    {field.name}: {field.value}')
                if 'reviewer_' in field.name:
                    if field.value not in curators:
                        # Add a new curator to the list if they're not already there
                        # The value of the reviewer_x custom field in trello must be a trello username
                        curators[field.value] = {'id': '', 'total_items': 0, 'total_time': 0,
                                                 'easy_items': 0, 'easy_time': 0, 'med_items': 0, 'med_time': 0,'hard_items': 0, 'hard_time': 0,
                                                 '3M_items' :0, '3M_time': 0}
                        for member in boardmembers:
                            # Extract the id from the username
                            if member.username == field.value:
                                curators[field.value]['id'] = member.id

                    curators[field.value]['total_items'] += 1
            
            print()
            for plugin in card.plugin_data:
                if plugin['idPlugin'] == '5c592ae4d74ac4407f4e3af3':
                    # Get the recorded time from the Activity powerup (convert from milliseconds to seconds)
                    powerup_timedata = literal_eval(plugin['value'])['users']
                    for username, curator in curators.items():
                        if curator['id'] in powerup_timedata:
                            curator['total_time'] += int(powerup_timedata[curator['id']]['time'])/1000
                            
                    print(f'    {powerup_timedata}')
                
    except Exception as e:
        tb_list = traceback.extract_tb(sys.exc_info()[2])
        line_number = tb_list[-1][1]
        print(f'Error getting board info: {e}, line {line_number}')
        return {}

    print('Curation stats for items published since Jan 1, 2025')

    outfile = None
    if args.outfile:
        outfile = f.get_report_outfile(args.outfile, 'curators')
        outfile.write(
            f'username,total_items,total_time ({args.units}),'
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
        print(f'username \t total_items \t total_time ({args.units})')

    total_time = 0
    total_items = 0

    for username, curator in curators.items():
        if outfile:
            pass
        else:
            s = '{0} \t {1} \t\t {2}'
            
        s = s.format(username, curator['total_items'], f.format_duration(str(curator['total_time'])+'s', args.units))
        
        total_time += curator['total_time']
        total_items += curator['total_items']

        if outfile:
            outfile.write(s + '\n')
        elif not args.sync_to_dashboard:
            print(s)

    print(f'Total curation hours:\t\t\t\t{f.format_duration(str(total_time)+'s', 'H')}')
    print(f'Avg items per curator (primary or secondary):\t{total_items / len(curators)}')

    if outfile:
        outfile.close()

    return curators
