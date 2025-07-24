# -*- coding: utf-8 -*-

# Runs various reports for ReDATA
#
# Author: Fernando Rios

import argparse
import sys
from os import environ
from version import __version__, __commit__

sys.path.insert(0, 'lib/')
import curator_report
import functions as f
import secrets


def init_argparse():
    parser = argparse.ArgumentParser(
        description='Runs reports for Trello stats'
    )
    parser.add_argument(
        '-r', '--report', required=False, action='append', choices=['curators', 'items'],
        help="Selects which report to run. This option can appear more than once"
    )
    parser.add_argument(
        '--sync-to-dashboard', required=False, action='store_true',
        help="Uploads report data to the Google dashboard. Additionally, sets these flags: -u B -r items -r users"
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version=f'{parser.prog} v{__version__} {__commit__}'
    )
    parser.add_argument(
        '-o', '--outfile', metavar='PATH', nargs='?',
        const=f"$$*$${f.get_report_date().strftime('%Y-%m-%dT%H%M%S')}.csv",
        type=str, help="Write output to a file. If PATH isn't specified, file will default to a timestamped file in the current directory"
    )
    parser.add_argument(
        '-u', '--units', choices=['M', 'W', 'D', 'H', 'm', 's'],
        default='H', help='Set the output time units. Default is %(default)s')

    return parser


def run(args):
    print(f'This is trello-reports version v{__version__} {__commit__}')

    if args.sync_to_dashboard:
        args.units = 's'
        args.report = ['curators', 'items']

    if not args.report:
        return 'No report specified. Doing nothing'

    result = ''
    if 'curators' in args.report:
        print('Running "curators" report')
        data = curator_report.run(args)
        result = result + f'Running "curator" report completed. {len(data)} curators.'
        if args.sync_to_dashboard:
            result = result + f'\nSyncing "curator" to dashboard completed. Result: {f.sync_to_dashboard(data, "curator")}.'
    if 'items' in args.report:
        print('Running "items" report')
        result = 'not implemented'

    return result


if __name__ == '__main__':
    args = init_argparse().parse_args()

    environ['API_TRELLO_URL_BASE'] = secrets.api_trello_url_base
    environ['API_TRELLO_KEY'] = secrets.api_trello_key
    environ['API_TRELLO_TOKEN'] = secrets.api_trello_token
    environ['TRELLO_BOARD_ID'] = secrets.trello_board_id
    environ['TRELLO_PUBLISHEDLIST_ID'] = secrets.trello_publishedlist_id
    environ['GSHEETS_DASHBOARD_POST_URL'] = secrets.gsheets_dashboard_post_url
    environ['GSHEETS_DASHBOARD_KEY'] = secrets.gsheets_dashboard_key
    environ['TOKEN'] = secrets.do_token

    print(run(args))
