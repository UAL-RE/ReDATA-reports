# -*- coding: utf-8 -*-

# Prints the usage for each public dataset
#
# Author: Fernando Rios

import sys
import traceback
from ast import literal_eval
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil.tz import tzlocal
from os import environ
from trello import TrelloClient

sys.path.insert(0, 'lib/')
import functions as f

debug = 0  # 0 = off, 1 = print card name + output cards to cards.csv, 2 = 1 + print more card info, 3 = 2 + card filter results
tc = None
currdate = datetime.now(tzlocal())


def get_card_curators(card, existing_curators: dict[str, any] = None):
    """
    Returns the curators for the given Card object as a list of Trello usernames.

    If the existing_curators dictionary is passed in, if a curator is found that does not exist in the
    dictionary, a new entry is created with the key equal to the value of the reviewer_N custom field (N is an integer).
    Currently it is the value of the Trello username.
    """

    curators = []

    if debug > 0:
        print(card.name)

    for field in card.custom_fields:
        if 'reviewer_' in field.name:
            if debug > 1:
                print(f'    {field.name}: {field.value}')

            curators.append(field.value)

            if type(existing_curators) is dict and field.value not in existing_curators:
                # Add a new curator to the list if they're not already there
                # The value of the reviewer_x custom field in trello must be a trello username
                existing_curators[field.value] = {
                    'username': field.value, 'id': '', 'total_items': 0, 'total_time': 0,
                    'easy_items': 0, 'easy_time': 0, 'med_items': 0, 'med_time': 0, 'hard_items': 0, 'hard_time': 0,
                    '3M_items': 0, '3M_time': 0,
                    '6M_items': 0, '6M_time': 0,
                    '1Y_items': 0, '1Y_time': 0,
                    '2Y_items': 0, '2Y_time': 0,
                    '3M_easy_items': 0, '3M_easy_time': 0,
                    '3M_med_items': 0, '3M_med_time': 0,
                    '3M_hard_items': 0, '3M_hard_time': 0,
                    '6M_easy_items': 0, '6M_easy_time': 0,
                    '6M_med_items': 0, '6M_med_time': 0,
                    '6M_hard_items': 0, '6M_hard_time': 0,
                    '1Y_easy_items': 0, '1Y_easy_time': 0,
                    '1Y_med_items': 0, '1Y_med_time': 0,
                    '1Y_hard_items': 0, '1Y_hard_time': 0,
                    '2Y_easy_items': 0, '2Y_easy_time': 0,
                    '2Y_med_items': 0, '2Y_med_time': 0,
                    '2Y_hard_items': 0, '2Y_hard_time': 0,
                    'total_reviewer1_items': 0, 'total_reviewer1_time': 0,
                    'total_reviewer2_items': 0, 'total_reviewer2_time': 0,
                    'easy_reviewer1_items': 0, 'easy_reviewer1_time': 0,
                    'easy_reviewer2_items': 0, 'easy_reviewer2_time': 0,
                    'med_reviewer1_items': 0, 'med_reviewer1_time': 0,
                    'med_reviewer2_items': 0, 'med_reviewer2_time': 0,
                    'hard_reviewer1_items': 0, 'hard_reviewer1_time': 0,
                    'hard_reviewer2_items': 0, 'hard_reviewer2_time': 0,
                    '3M_reviewer1_items': 0, '3M_reviewer1_time': 0,
                    '3M_reviewer2_items': 0, '3M_reviewer2_time': 0,
                    '6M_reviewer1_items': 0, '6M_reviewer1_time': 0,
                    '6M_reviewer2_items': 0, '6M_reviewer2_time': 0,
                    '1Y_reviewer1_items': 0, '1Y_reviewer1_time': 0,
                    '1Y_reviewer2_items': 0, '1Y_reviewer2_time': 0,
                    '2Y_reviewer1_items': 0, '2Y_reviewer1_time': 0,
                    '2Y_reviewer2_items': 0, '2Y_reviewer2_time': 0,
                    '3M_easy_reviewer1_items': 0, '3M_easy_reviewer1_time': 0,
                    '3M_easy_reviewer2_items': 0, '3M_easy_reviewer2_time': 0,
                    '6M_easy_reviewer1_items': 0, '6M_easy_reviewer1_time': 0,
                    '6M_easy_reviewer2_items': 0, '6M_easy_reviewer2_time': 0,
                    '1Y_easy_reviewer1_items': 0, '1Y_easy_reviewer1_time': 0,
                    '1Y_easy_reviewer2_items': 0, '1Y_easy_reviewer2_time': 0,
                    '2Y_easy_reviewer1_items': 0, '2Y_easy_reviewer1_time': 0,
                    '2Y_easy_reviewer2_items': 0, '2Y_easy_reviewer2_time': 0,
                    '3M_med_reviewer1_items': 0, '3M_med_reviewer1_time': 0,
                    '3M_med_reviewer2_items': 0, '3M_med_reviewer2_time': 0,
                    '6M_med_reviewer1_items': 0, '6M_med_reviewer1_time': 0,
                    '6M_med_reviewer2_items': 0, '6M_med_reviewer2_time': 0,
                    '1Y_med_reviewer1_items': 0, '1Y_med_reviewer1_time': 0,
                    '1Y_med_reviewer2_items': 0, '1Y_med_reviewer2_time': 0,
                    '2Y_med_reviewer1_items': 0, '2Y_med_reviewer1_time': 0,
                    '2Y_med_reviewer2_items': 0, '2Y_med_reviewer2_time': 0,
                    '3M_hard_reviewer1_items': 0, '3M_hard_reviewer1_time': 0,
                    '3M_hard_reviewer2_items': 0, '3M_hard_reviewer2_time': 0,
                    '6M_hard_reviewer1_items': 0, '6M_hard_reviewer1_time': 0,
                    '6M_hard_reviewer2_items': 0, '6M_hard_reviewer2_time': 0,
                    '1Y_hard_reviewer1_items': 0, '1Y_hard_reviewer1_time': 0,
                    '1Y_hard_reviewer2_items': 0, '1Y_hard_reviewer2_time': 0,
                    '2Y_hard_reviewer1_items': 0, '2Y_hard_reviewer1_time': 0,
                    '2Y_hard_reviewer2_items': 0, '2Y_hard_reviewer2_time': 0,
                    'report_date': f.get_report_date().strftime('%Y-%m-%d %H:%M:%S')
                }

                for member in tc.get_board(card.board_id).all_members():
                    # Extract the id from the username
                    if member.username == field.value:
                        existing_curators[field.value]['id'] = member.id

    if debug > 1:
        for plugin in card.plugin_data:
            if plugin['idPlugin'] == '5c592ae4d74ac4407f4e3af3':
                powerup_timedata = literal_eval(plugin['value'])['users']
                print(f'    timedata: {powerup_timedata}')

    return curators


def get_card_time(card, userid: str = None):
    """
    Returns the total time in seconds from the Activity powerup for this card.
    If userid is given, limits the time to only the given userid
    """

    total = 0

    for plugin in card.plugin_data:
        if plugin['idPlugin'] == '5c592ae4d74ac4407f4e3af3':
            powerup_timedata = literal_eval(plugin['value'])['users']
            for id, timedata in powerup_timedata.items():
                if userid and userid == id:
                    total = int(timedata['time']) / 1000
                if not userid:
                    total += int(timedata['time']) / 1000
    return total


def curator_items_time(existing_curators: dict[str, any], curators_field_prefix: str, card, cardfilter: dict[str, str] = None):
    """
    For the given curators dictionary as generated by get_card_curators

    - Increments the [curators_field_prefix]_items count for each curator that contributed to the given card.
    - Increments the [curators_field_prefix]_time value (in seconds) for each curator that contributed to the given card.
      The increment is based on the logged time for that curator.
    - Applies the operations only if the card meets ALL the criteria specified in cardfilter. If None, the operation is always applied.

    existing_curators is a dict set up by get_card_curators
    """

    if debug > 2:
        print(f'cardfilter: {cardfilter}')

    # Turn the custom fields into a dict for ease of use
    customfields = {}
    for field in card.custom_fields:
        customfields[field.name] = field.value

    include_card = False
    filter_result = 'NoFilter'
    if not cardfilter:
        include_card = True
    else:
        filter_result = {}
        for name, value in cardfilter.items():
            filter_result[name] = False
            match name:
                case 'difficulty':
                    if name in customfields.keys() and value == customfields[name]:
                        filter_result[name] = True

                    if debug > 2:
                        print(f'      {name} filter: result={filter_result[name]} | '
                              + f'requested_difficulty={value} card_difficulty={customfields[name] if name in customfields.keys() else None}')
                case 'published_date':
                    pubdate = ''
                    cutoffdate = ''
                    if name in customfields.keys():
                        pubdate = parse(customfields[name])
                        cutoffdate = currdate - relativedelta(months=float(value))
                        if pubdate and pubdate >= cutoffdate:
                            filter_result[name] = True

                    if debug > 2:
                        print(f'      {name} filter: result={filter_result[name]} | '
                              + f'card_pubdate={str(pubdate)} >= cutoff_date={str(cutoffdate)}')
                case 'reviewer_1' | 'reviewer_2':
                    if name in customfields.keys():
                        filter_result[name] = True

            include_card = all(filter_result.values())

    if debug > 2:
        print(f'    include_card: {include_card} | {filter_result}')
        print('     ---')

    if include_card:
        for username, curator in existing_curators.items():
            reviewer1_id = ''
            reviewer2_id = ''

            # Item counts for each curator, based on card filter criteria
            for fieldname, fieldvalue in customfields.items():
                if 'reviewer_' in fieldname and username in fieldvalue:

                    # Add to the item count, whether the curator was reviewer 1 or reviewer 2
                    curator[curators_field_prefix + '_items'] += 1

                    # Now, add to the specific reviewer 1 or 2 counts for the given curator
                    # and record whether that curator was reviewer 1 or 2.
                    if 'reviewer_1' in fieldname and username in fieldvalue:
                        curator[curators_field_prefix + '_reviewer1_items'] += 1
                        reviewer1_id = curator['id']
                    if 'reviewer_2' in fieldname and username in fieldvalue:
                        curator[curators_field_prefix + '_reviewer2_items'] += 1
                        reviewer2_id = curator['id']

            # Time for each curator, based on card filter criteria
            curator[curators_field_prefix + '_time'] += get_card_time(card, curator['id'])

            # Record time for the appropriate reviewer1 or reviewer2 categories for this curator (if this curator worked on the item)
            if reviewer1_id:
                curator[curators_field_prefix + '_reviewer1_time'] += get_card_time(card, reviewer1_id)
            if reviewer2_id:
                curator[curators_field_prefix + '_reviewer2_time'] += get_card_time(card, reviewer2_id)


def curator_total_items_time(existing_curators: dict[str, any], card):
    return curator_items_time(existing_curators, 'total', card, None)


def curator_easy_items_time(existing_curators: dict[str, any], card):
    # All items with difficulty=easy
    return curator_items_time(existing_curators, 'easy', card, {'difficulty': 'easy'})


def curator_med_items_time(existing_curators: dict[str, any], card):
    # All items with difficulty=medium
    return curator_items_time(existing_curators, 'med', card, {'difficulty': 'medium'})


def curator_hard_items_time(existing_curators: dict[str, any], card):
    # All items with difficulty=hard
    return curator_items_time(existing_curators, 'hard', card, {'difficulty': 'hard'})


def curator_3m_items_time(existing_curators: dict[str, any], card):
    # All items published in last 3 months
    return curator_items_time(existing_curators, '3M', card, {'published_date': 3})


def curator_6m_items_time(existing_curators: dict[str, any], card):
    # All items published in last 6 months
    return curator_items_time(existing_curators, '6M', card, {'published_date': 6})


def curator_1y_items_time(existing_curators: dict[str, any], card):
    # All items published in last year
    return curator_items_time(existing_curators, '1Y', card, {'published_date': 12})


def curator_2y_items_time(existing_curators: dict[str, any], card):
    # All items published in last 2 years
    return curator_items_time(existing_curators, '2Y', card, {'published_date': 24})


def curator_3m_easy_items_time(existing_curators: dict[str, any], card):
    # All easy items published in last 3 months
    return curator_items_time(existing_curators, '3M_easy', card, {'difficulty': 'easy', 'published_date': 3})


def curator_6m_easy_items_time(existing_curators: dict[str, any], card):
    # All easy items published in last 6 months
    return curator_items_time(existing_curators, '6M_easy', card, {'difficulty': 'easy', 'published_date': 6})


def curator_1y_easy_items_time(existing_curators: dict[str, any], card):
    # All easy items published in last year
    return curator_items_time(existing_curators, '1Y_easy', card, {'difficulty': 'easy', 'published_date': 12})


def curator_2y_easy_items_time(existing_curators: dict[str, any], card):
    # All easy items published in last 2 years
    return curator_items_time(existing_curators, '2Y_easy', card, {'difficulty': 'easy', 'published_date': 24})


def curator_3m_med_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 3 months
    return curator_items_time(existing_curators, '3M_med', card, {'difficulty': 'medium', 'published_date': 3})


def curator_6m_med_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 6 months
    return curator_items_time(existing_curators, '6M_med', card, {'difficulty': 'medium', 'published_date': 6})


def curator_1y_med_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last year
    return curator_items_time(existing_curators, '1Y_med', card, {'difficulty': 'medium', 'published_date': 12})


def curator_2y_med_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 2 years
    return curator_items_time(existing_curators, '2Y_med', card, {'difficulty': 'medium', 'published_date': 24})


def curator_3m_hard_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 3 months
    return curator_items_time(existing_curators, '3M_hard', card, {'difficulty': 'hard', 'published_date': 3})


def curator_6m_hard_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 6 months
    return curator_items_time(existing_curators, '6M_hard', card, {'difficulty': 'hard', 'published_date': 6})


def curator_1y_hard_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last year
    return curator_items_time(existing_curators, '1Y_hard', card, {'difficulty': 'hard', 'published_date': 12})


def curator_2y_hard_items_time(existing_curators: dict[str, any], card):
    # All medium items published in last 2 years
    return curator_items_time(existing_curators, '2Y_hard', card, {'difficulty': 'hard', 'published_date': 24})


def run(args):
    # Optionally writes a CSV report to file and returns a JSON array of objects with the data that was written.

    global tc
    curators = {}

    print('Getting curator stats from Trello')

    tc = TrelloClient(api_key=environ['API_TRELLO_KEY'], api_secret=environ['API_TRELLO_TOKEN'])

    try:
        board = tc.get_board(environ['TRELLO_BOARD_ID'])
        cards = board.get_cards(filters=f.get_cardlist_filter()['query'])

        if len(cards) >= 1000:
            raise Exception("Trello API returned 1000 cards. Pagination may be needed but is not yet implemented")

        # Preprocess board cards to filter out the ones without published_date set.
        # Do it this way instead of by returning only cards from the Published list so that
        # we grab cards in other lists that may have been published already but have been moved to another list.
        publishedcards = []
        fl = None

        if debug > 0:
            fl = open('cards.csv', 'w', encoding="utf-8")

        if fl:
            fl.write(
                'name,difficulty,total_time_mins,article_version,article_revision,'
                + 'reviewer_1,reviewer_2,submission_date,forms_sent_date,reviewed_date,published_date,keep?\n')
        for card in cards:
            # Turn the custom fields into a dict for ease of use
            customfields = {}
            for field in card.custom_fields:
                customfields[field.name] = field.value
            keep = True if not customfields.get('published_date', '') == '' else False

            if keep:
                publishedcards.append(card)

            if fl:
                fl.write(
                    '"' + card.name.replace('"', '""') + '",'
                    + customfields.get('difficulty', '""') + ','
                    + str(customfields.get('total_time_mins', '""')) + ','
                    + str(customfields.get('article_version', '""')) + ',' + str(customfields.get('article_revision', '""')) + ','
                    + str(customfields.get('reviewer_1', '""')) + ',' + str(customfields.get('reviewer_2', '""')) + ','
                    + str(customfields.get('submission_date', '""')) + ',' + str(customfields.get('forms_sent_date', '""')) + ','
                    + str(customfields.get('reviewed_date', '""')) + ',' + str(customfields.get('published_date', '""')) + ','
                    + f'{keep}\n')
        if fl:
            fl.close()

        for card in publishedcards:
            # Preprocess the card to get the reviewers
            get_card_curators(card, curators)

            curator_total_items_time(curators, card)
            curator_easy_items_time(curators, card)
            curator_med_items_time(curators, card)
            curator_hard_items_time(curators, card)
            curator_3m_items_time(curators, card)
            curator_6m_items_time(curators, card)
            curator_1y_items_time(curators, card)
            curator_2y_items_time(curators, card)
            curator_3m_easy_items_time(curators, card)
            curator_6m_easy_items_time(curators, card)
            curator_1y_easy_items_time(curators, card)
            curator_2y_easy_items_time(curators, card)
            curator_3m_med_items_time(curators, card)
            curator_6m_med_items_time(curators, card)
            curator_1y_med_items_time(curators, card)
            curator_2y_med_items_time(curators, card)
            curator_3m_hard_items_time(curators, card)
            curator_6m_hard_items_time(curators, card)
            curator_1y_hard_items_time(curators, card)
            curator_2y_hard_items_time(curators, card)
        print()

    except Exception as e:
        tb_list = traceback.extract_tb(sys.exc_info()[2])
        line_number = tb_list[-1][1]
        print(f'Error getting board data: {e}, line {line_number}')
        return {}

    print(f'Curation stats for items (and versions) published {f.get_cardlist_filter()["description"]}')
    print(f'Processed {len(publishedcards)} cards with published_date set, out of {len(cards)} fetched')

    outfile = None
    if args.outfile:
        outfile = f.get_report_outfile(args.outfile, 'curators')
        outfile.write(
            f'username,total_items,total_time ({args.units}),'
            + f'easy_items,easy_time ({args.units}),med_items,med_time ({args.units}),hard_items,hard_time ({args.units}),'
            + f'3M_items,3M_time ({args.units}),6M_items,6M_time ({args.units}),'
            + f'1Y_items,1Y_time ({args.units}),2Y_items,2Y_time ({args.units}),'
            + f'3M_easy_items,3M_easy_time ({args.units}),3M_med_items,3M_med_time ({args.units}),'
            + f'3M_hard_items,3M_hard_time ({args.units}),6M_easy_items,6M_easy_time ({args.units}),'
            + f'6M_med_items,6M_med_time ({args.units}),6M_hard_items,6M_hard_time ({args.units}),'
            + f'1Y_easy_items,1Y_easy_time ({args.units}),1Y_med_items,1Y_med_time ({args.units}),'
            + f'1Y_hard_items,1Y_hard_time ({args.units}),2Y_easy_items,2Y_easy_time ({args.units}),'
            + f'2Y_med_items,2Y_med_time ({args.units}),2Y_hard_items,2Y_hard_time ({args.units}),'
            + f'total_reviewer1_items,total_reviewer1_time ({args.units}),'
            + f'total_reviewer2_items,total_reviewer2_time ({args.units}),'
            + f'3M_reviewer1_items,3M_reviewer1_time ({args.units}),'
            + f'3M_reviewer2_items,3M_reviewer2_time ({args.units}),'
            + f'6M_reviewer1_items,6M_reviewer1_time ({args.units}),'
            + f'6M_reviewer2_items,6M_reviewer2_time ({args.units}),'
            + f'1Y_reviewer1_items,1Y_reviewer1_time ({args.units}),'
            + f'1Y_reviewer2_items,1Y_reviewer2_time ({args.units}),'
            + f'2Y_reviewer1_items,2Y_reviewer1_time ({args.units}),'
            + f'2Y_reviewer2_items,2Y_reviewer2_time ({args.units}),'
            + f'3M_easy_reviewer1_items,3M_easy_reviewer1_time ({args.units}),'
            + f'3M_easy_reviewer2_items,3M_easy_reviewer2_time ({args.units}),'
            + f'3M_med_reviewer1_items,3M_med_reviewer1_time ({args.units}),'
            + f'3M_med_reviewer2_items,3M_med_reviewer2_time ({args.units}),'
            + f'3M_hard_reviewer1_items,3M_hard_reviewer1_time ({args.units}),'
            + f'3M_hard_reviewer2_items,3M_hard_reviewer2_time ({args.units}),'
            + f'6M_easy_reviewer1_items,6M_easy_reviewer1_time ({args.units}),'
            + f'6M_easy_reviewer2_items,6M_easy_reviewer2_time ({args.units}),'
            + f'6M_med_reviewer1_items,6M_med_reviewer1_time ({args.units}),'
            + f'6M_med_reviewer2_items,6M_med_reviewer2_time ({args.units}),'
            + f'6M_hard_reviewer1_items,6M_hard_reviewer1_time ({args.units}),'
            + f'6M_hard_reviewer2_items,6M_hard_reviewer2_time ({args.units}),'
            + f'1Y_easy_reviewer1_items,1Y_easy_reviewer1_time ({args.units}),'
            + f'1Y_easy_reviewer2_items,1Y_easy_reviewer2_time ({args.units}),'
            + f'1Y_med_reviewer1_items,1Y_med_reviewer1_time ({args.units}),'
            + f'1Y_med_reviewer2_items,1Y_med_reviewer2_time ({args.units}),'
            + f'1Y_hard_reviewer1_items,1Y_hard_reviewer1_time ({args.units}),'
            + f'1Y_hard_reviewer2_items,1Y_hard_reviewer2_time ({args.units}),'
            + f'2Y_easy_reviewer1_items,2Y_easy_reviewer1_time ({args.units}),'
            + f'2Y_easy_reviewer2_items,2Y_easy_reviewer2_time ({args.units}),'
            + f'2Y_med_reviewer1_items,2Y_med_reviewer1_time ({args.units}),'
            + f'2Y_med_reviewer2_items,2Y_med_reviewer2_time ({args.units}),'
            + f'2Y_hard_reviewer1_items,2Y_hard_reviewer1_time ({args.units}),'
            + f'2Y_hard_reviewer2_items,2Y_hard_reviewer2_time ({args.units}),'
            + '\n')

    elif not args.sync_to_dashboard:
        print(
            f'username\ttot_itms\ttot_tm({args.units})\tlast 3m itms\tlast 3m tm({args.units})'
            + f' rvwr1_itms rvwr1_tm({args.units})'
            + f' rvwr2_itms rvwr2_tm({args.units})')

    total_time = 0
    total_items = 0

    for username, curator in curators.items():
        if outfile:
            s = (
            '{0},{1},{2},'                # username, total items, total time
            + '{3},{4},{5},{6},{7},{8},'  # easy, med, hard items & time
            + '{9},{10},{11},{12},'       # 3M, 6M items & time
            + '{13},{14},{15},{16},'      # 1Y, 2Y items & time
            + '{17},{18},{19},{20},'      # 3M_easy, 3M_med items & time
            + '{21},{22},{23},{24},'      # 3M_hard, 6M_easy items & time
            + '{25},{26},{27},{28},'      # 6M_med, 6M_hard items & time
            + '{29},{30},{31},{32},'      # 1Y_easy, 1Y_med items & time
            + '{33},{34},{35},{36},'      # 1Y_hard, 2Y_easy items & time
            + '{37},{38},{39},{40},'      # 2Y_med, 2Y_hard items & time
            + '{41},{42},{43},{44},'      # total reviewer_1, reviewer_2 items & time
            + '{45},{46},{47},{48},'      # 3M reviewer_1, reviewer_2 items & time
            + '{49},{50},{51},{52},'      # 6M reviewer_1, reviewer_2 items & time
            + '{53},{54},{55},{56},'      # 1Y reviewer_1, reviewer_2 items & time
            + '{57},{58},{59},{60},'      # 2Y reviewer_1, reviewer_2 items & time
            + '{61},{62},{63},{64},'      # 3M_easy reviewer_1, reviewer_2 items & time
            + '{65},{66},{67},{68},'      # 3M_med reviewer_1, reviewer_2 items & time
            + '{69},{70},{71},{72},'      # 3M_hard reviewer_1, reviewer_2 items & time
            + '{73},{74},{75},{76},'      # 6M_easy reviewer_1, reviewer_2 items & time
            + '{77},{78},{79},{80},'      # 6M_med reviewer_1, reviewer_2 items & time
            + '{81},{82},{83},{84},'      # 6M_hard reviewer_1, reviewer_2 items & time
            + '{85},{86},{87},{88},'      # 1Y_easy reviewer_1, reviewer_2 items & time
            + '{89},{90},{91},{92},'      # 1Y_med reviewer_1, reviewer_2 items & time
            + '{93},{94},{95},{96},'      # 1Y_hard reviewer_1, reviewer_2 items & time
            + '{97},{98},{99},{100},'     # 2Y_easy reviewer_1, reviewer_2 items & time
            + '{101},{102},{103},{104},'  # 2Y_med reviewer_1, reviewer_2 items & time
            + '{105},{106},{107},{108}'   # 2Y_hard reviewer_1, reviewer_2 items & time
            )
        else:
            s = ('{0} \t'
                 + '{1} \t\t {2} \t\t'
                 + '{9} \t\t {10} \t\t'
                 + '{41}\t {42}\t\t{43}\t{44}')

        s = s.format(
            username,                                                                                 # 0
            curator['total_items'], f.format_duration(str(curator['total_time']) + 's', args.units),  # 1,2
            curator['easy_items'], f.format_duration(str(curator['easy_time']) + 's', args.units),    # 3,4
            curator['med_items'], f.format_duration(str(curator['med_time']) + 's', args.units),      # 5,6
            curator['hard_items'], f.format_duration(str(curator['hard_time']) + 's', args.units),    # 7,8
            curator['3M_items'], f.format_duration(str(curator['3M_time']) + 's', args.units),        # 9,10
            curator['6M_items'], f.format_duration(str(curator['6M_time']) + 's', args.units),        # 11,12
            curator['1Y_items'], f.format_duration(str(curator['1Y_time']) + 's', args.units),        # 13,14
            curator['2Y_items'], f.format_duration(str(curator['2Y_time']) + 's', args.units),        # 15,16
            curator['3M_easy_items'], f.format_duration(str(curator['3M_easy_time']) + 's', args.units),       # 17,18
            curator['3M_med_items'], f.format_duration(str(curator['3M_med_time']) + 's', args.units),         # 19,20
            curator['3M_hard_items'], f.format_duration(str(curator['3M_hard_time']) + 's', args.units),       # 21,22
            curator['6M_easy_items'], f.format_duration(str(curator['6M_easy_time']) + 's', args.units),       # 23,24
            curator['6M_med_items'], f.format_duration(str(curator['6M_med_time']) + 's', args.units),         # 25,26
            curator['6M_hard_items'], f.format_duration(str(curator['6M_hard_time']) + 's', args.units),       # 27,28
            curator['1Y_easy_items'], f.format_duration(str(curator['1Y_easy_time']) + 's', args.units),       # 29,30
            curator['1Y_med_items'], f.format_duration(str(curator['1Y_med_time']) + 's', args.units),         # 31,32
            curator['1Y_hard_items'], f.format_duration(str(curator['1Y_hard_time']) + 's', args.units),       # 33,34
            curator['2Y_easy_items'], f.format_duration(str(curator['2Y_easy_time']) + 's', args.units),       # 35,36
            curator['2Y_med_items'], f.format_duration(str(curator['2Y_med_time']) + 's', args.units),         # 37,38
            curator['2Y_hard_items'], f.format_duration(str(curator['2Y_hard_time']) + 's', args.units),       # 39,40
            curator['total_reviewer1_items'], f.format_duration(str(curator['total_reviewer1_time']) + 's', args.units),   # 41,42
            curator['total_reviewer2_items'], f.format_duration(str(curator['total_reviewer2_time']) + 's', args.units),   # 43,44
            curator['3M_reviewer1_items'], f.format_duration(str(curator['3M_reviewer1_time']) + 's', args.units),   # 45,46
            curator['3M_reviewer2_items'], f.format_duration(str(curator['3M_reviewer2_time']) + 's', args.units),   # 47,48
            curator['6M_reviewer1_items'], f.format_duration(str(curator['6M_reviewer1_time']) + 's', args.units),   # 49,50
            curator['6M_reviewer2_items'], f.format_duration(str(curator['6M_reviewer2_time']) + 's', args.units),   # 51,52
            curator['1Y_reviewer1_items'], f.format_duration(str(curator['1Y_reviewer1_time']) + 's', args.units),   # 53,54
            curator['1Y_reviewer2_items'], f.format_duration(str(curator['1Y_reviewer2_time']) + 's', args.units),   # 55,56
            curator['2Y_reviewer1_items'], f.format_duration(str(curator['2Y_reviewer1_time']) + 's', args.units),   # 57,58
            curator['2Y_reviewer2_items'], f.format_duration(str(curator['2Y_reviewer2_time']) + 's', args.units),   # 59,60
            curator['3M_easy_reviewer1_items'], f.format_duration(str(curator['3M_easy_reviewer1_time']) + 's', args.units),   # 61,62
            curator['3M_easy_reviewer2_items'], f.format_duration(str(curator['3M_easy_reviewer2_time']) + 's', args.units),   # 63,64
            curator['3M_med_reviewer1_items'], f.format_duration(str(curator['3M_med_reviewer1_time']) + 's', args.units),     # 65,66
            curator['3M_med_reviewer2_items'], f.format_duration(str(curator['3M_med_reviewer2_time']) + 's', args.units),     # 67,68
            curator['3M_hard_reviewer1_items'], f.format_duration(str(curator['3M_hard_reviewer1_time']) + 's', args.units),   # 69,70
            curator['3M_hard_reviewer2_items'], f.format_duration(str(curator['3M_hard_reviewer2_time']) + 's', args.units),   # 71,72
            curator['6M_easy_reviewer1_items'], f.format_duration(str(curator['6M_easy_reviewer1_time']) + 's', args.units),   # 73,74
            curator['6M_easy_reviewer2_items'], f.format_duration(str(curator['6M_easy_reviewer2_time']) + 's', args.units),   # 75,76
            curator['6M_med_reviewer1_items'], f.format_duration(str(curator['6M_med_reviewer1_time']) + 's', args.units),     # 77,78
            curator['6M_med_reviewer2_items'], f.format_duration(str(curator['6M_med_reviewer2_time']) + 's', args.units),     # 79,80
            curator['6M_hard_reviewer1_items'], f.format_duration(str(curator['6M_hard_reviewer1_time']) + 's', args.units),   # 81,82
            curator['6M_hard_reviewer2_items'], f.format_duration(str(curator['6M_hard_reviewer2_time']) + 's', args.units),   # 83,84
            curator['1Y_easy_reviewer1_items'], f.format_duration(str(curator['1Y_easy_reviewer1_time']) + 's', args.units),   # 85,86
            curator['1Y_easy_reviewer2_items'], f.format_duration(str(curator['1Y_easy_reviewer2_time']) + 's', args.units),   # 87,88
            curator['1Y_med_reviewer1_items'], f.format_duration(str(curator['1Y_med_reviewer1_time']) + 's', args.units),     # 89,90
            curator['1Y_med_reviewer2_items'], f.format_duration(str(curator['1Y_med_reviewer2_time']) + 's', args.units),     # 91,92
            curator['1Y_hard_reviewer1_items'], f.format_duration(str(curator['1Y_hard_reviewer1_time']) + 's', args.units),   # 93,94
            curator['1Y_hard_reviewer2_items'], f.format_duration(str(curator['1Y_hard_reviewer2_time']) + 's', args.units),   # 95,96
            curator['2Y_easy_reviewer1_items'], f.format_duration(str(curator['2Y_easy_reviewer1_time']) + 's', args.units),   # 97,98
            curator['2Y_easy_reviewer2_items'], f.format_duration(str(curator['2Y_easy_reviewer2_time']) + 's', args.units),   # 99,100
            curator['2Y_med_reviewer1_items'], f.format_duration(str(curator['2Y_med_reviewer1_time']) + 's', args.units),     # 101,102
            curator['2Y_med_reviewer2_items'], f.format_duration(str(curator['2Y_med_reviewer2_time']) + 's', args.units),     # 103,104
            curator['2Y_hard_reviewer1_items'], f.format_duration(str(curator['2Y_hard_reviewer1_time']) + 's', args.units),   # 105,106
            curator['2Y_hard_reviewer2_items'], f.format_duration(str(curator['2Y_hard_reviewer2_time']) + 's', args.units)    # 107,108
            )

        total_time += curator['total_time']
        total_items += curator['total_items']

        if outfile:
            outfile.write(s + '\n')
        elif not args.sync_to_dashboard:
            print(s)

    print()
    print(f'Total curation hours:\t{f.format_duration(str(total_time) + "s", "H")}')
    print(f'Avg hours per item:\t{f.format_duration(str(total_time / total_items) + "s", "H")}')

    if outfile:
        outfile.close()

    return list(curators.values())
