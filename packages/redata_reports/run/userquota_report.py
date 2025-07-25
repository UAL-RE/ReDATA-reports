# -*- coding: utf-8 -*-

# Prints out used_quota, private_quota, public_quota, orcid_id for all accounts
# A November 2021 update to Figshare's API means you can now get the account quota, orcid, and
# the used_quota with a call to v2/account/institution/accounts. However, the new API
# Doesn't return the private or public quota and the ORCID id doesn't seem to show for all accounts.
# Therefore, this script is still the best way to get all info.
#
# Author: Fernando Rios

import sys
import requests
import simplejson as json
from multiprocessing import Pool
from os import environ

sys.path.insert(0, 'lib/')
import functions as f


def get_institution_accounts():
    page = 1
    accounts_list = []
    while True:
        api_url = '{0}/account/institution/accounts?page={1}&page_size=1000'.format(environ['API_FIGSHARE_URL_BASE'], page)
        page += 1
        response = requests.get(api_url, headers=f.get_request_headers())

        if response.status_code == 200:
            if response.text == '[]':
                return accounts_list
            accounts_list.extend(json.loads(response.text))
        else:
            print('Error. Response code {0}'.format(response.status_code))
            return None


def get_account_info(id):
    api_url = '{0}/account?impersonate={1}'.format(environ['API_FIGSHARE_URL_BASE'], id)
    response = requests.get(api_url, headers=f.get_request_headers())

    if response.status_code == 200:
        data = json.loads(response.text)
    elif response.status_code == 403:
        # can't impersonate ourselves
        api_url = '{0}/account'.format(environ['API_FIGSHARE_URL_BASE'])
        response = requests.get(api_url, headers=f.get_request_headers())
        data = json.loads(response.text)
    else:
        print('Error (/account?impersonate={1}), Response code {0}'.format(response.status_code, id))
        return ''

    if 'orcid_id' not in data:
        data['orcid_id'] = ''

    return data


def run(args):
    # Optionally writes a CSV report to file and returns a json array of objects with the data that was written.

    print('Getting institution account IDs')

    institution_accounts = get_institution_accounts()
    if institution_accounts is None:
        print('Request Failed.')
        return []
    print("total number found: {0}".format(len(institution_accounts)))

    account_ids = []
    for account in institution_accounts:
        account_ids.append(account['id'])

    print('Getting usage by account ID')

    accounts_info = []
    p = Pool(processes=5)
    result = p.map(get_account_info, account_ids)
    p.close()
    p.join()

    # get rid of any empty results and add timestamp
    for r in result:
        if len(r) > 0:
            r['report_date'] = f.get_report_date().strftime('%Y-%m-%d %H:%M:%S')
            accounts_info.append(r)

    total_usage = 0
    total_private_usage = 0
    total_public_usage = 0

    outfile = None
    if args.outfile:
        outfile = f.get_report_outfile(args.outfile, 'users')
        outfile.write(
            'email,quota {0},used_quota {0},private_quota {0},public_quota {0},public+private {0},orcid_id,group_id\n'.
            format(args.units))
    else:
        print(
            'email\t,quota {0}\t,used_quota_figshareUI {0}\t,private_quota {0}\t,public_quota {0}\t,public+private {0}\t,orcid_id\t,group_id'.
            format(args.units))

    for account in accounts_info:
        if outfile:
            s = '{0},{1},{2},{3},{4},{5},{6}'
        else:
            s = '{0}\t,{1}\t,{2}\t,{3}\t,{4}\t,{5}\t,{6}'

        s = s.format(account['email'],
                     f.format_bytes(account['quota'], args.units),
                     f.format_bytes(account['used_quota'], args.units),
                     f.format_bytes(account['used_quota_private'], args.units),
                     f.format_bytes(account['used_quota_public'], args.units),
                     f.format_bytes(account['used_quota_private'] + account['used_quota_public'], args.units),
                     account['orcid_id'],
                     account['group_id'])

        if outfile:
            outfile.write(s + '\n')
        elif not args.sync_to_dashboard:
            print(s)

        total_usage += account['used_quota']
        total_public_usage += account['used_quota_public']
        total_private_usage += account['used_quota_private']

    print()
    print('Unit\t\tTotal Usage,Total Public Usage,Total Private Usage')
    print('bytes,\t\t{0},\t{1},\t{2}'.format(total_usage, total_public_usage, total_private_usage))
    print('{3},\t\t{0},\t{1},\t{2}'.format(f.format_bytes(total_usage, args.units),
                                           f.format_bytes(total_public_usage, args.units),
                                           f.format_bytes(total_private_usage, args.units),
                                           args.units))

    if outfile:
        outfile.close()

    return accounts_info
