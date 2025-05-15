# -*- coding: utf-8 -*-

# Runs various reports for ReDATA
#
# Author: Fernando Rios

import argparse
from version import __version__, __commit__
import functions as f
import items_report
import userquota_report


def init_argparse():
    parser = argparse.ArgumentParser(
        description='Runs reports'
    )
    parser.add_argument(
        '-r', '--report', required=False, action='append', choices=['users', 'items'],
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
        '-u', '--units', choices=['B', 'KB', 'MB', 'GB', 'TB'],
        default='GB', help='Set the output units. Default is %(default)s')
        
    return parser


def run(args):
    if args.sync_to_dashboard:
        args.units = 'B'
        args.report = ['items', 'users']

    if not args.report:
        return 'No report specified. Doing nothing'

    result = ''
    if 'items' in args.report:
        print('Running "items" report')
        data = items_report.run(args)
        result = result + f'Running "items" report completed. {len(data)} items.'
        if args.sync_to_dashboard:             
            result = result + f'\nSyncing "items" to dashboard completed. Result: {f.sync_to_dashboard(data, "items")}.'
    if 'users' in args.report:
        print('Running "users" report')
        data = userquota_report.run(args)
        result = result + f'Running "users" report completed. {len(data)} users.'
        if args.sync_to_dashboard: 
            result = result + f'\nSyncing "users" to dashboard completed. Result: {f.sync_to_dashboard(data, "users")}.'

    return result


if __name__ == '__main__':    
    args = init_argparse().parse_args()
    print(run(args))

