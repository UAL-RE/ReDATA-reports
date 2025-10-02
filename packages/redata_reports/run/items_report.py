# -*- coding: utf-8 -*-

# Prints the usage for each public dataset
#
# Author: Fernando Rios

import sys
import requests
import simplejson as json
from multiprocessing import Pool
from datetime import datetime
from os import environ

sys.path.insert(0, 'lib/')
import functions as f


def get_institution_articles():
    page = 1
    article_list = []
    while True:
        api_url = '{0}/account/institution/articles?page={1}&page_size=1000'.format(environ['API_FIGSHARE_URL_BASE'], page)
        page += 1
        response = requests.get(api_url, headers=f.get_request_headers())

        if response.status_code == 200:
            if response.text == '[]':
                return article_list
            article_list.extend(json.loads(response.text))
        else:
            print('Error. Response code {0}'.format(response.status_code))
            return None


def get_public_article_info(article_ids):
    article_info = []
    unpublished_article_ids = []

    if type(article_ids) is str or type(article_ids) is int:
        article_ids = [article_ids]

    for id in article_ids:
        api_url = '{0}/articles/{1}/versions'.format(environ['API_FIGSHARE_URL_BASE'], id)
        response = requests.get(api_url, headers=f.get_request_headers())
        if response.status_code == 200:
            article_versions = json.loads(response.text)
            if len(article_versions) > 0:
                for version in article_versions:
                    version_num = version['version']
                    api_url = '{0}/articles/{1}/versions/{2}'.format(environ['API_FIGSHARE_URL_BASE'], id, version_num)
                    response = requests.get(api_url, headers=f.get_request_headers())

                    if response.status_code == 200:
                        article_info.append(json.loads(response.text))
                    else:
                        print('Error (/articles/{1}/versions/{2}), Response code {0}'.format(response.status_code, id, version_num))
            else:
                print(f"article {id} had no versions in public articles API. It was likely published and later unpublished.")
                unpublished_article_ids.append(id)

        else:
            print('Error getting article versions for {1}, Response code {0}'.format(id, response.status_code))

    return article_info, unpublished_article_ids


def get_private_article_info(article_ids):
    # only returns info for latest version. Use only for articles that are not public.

    article_info = []
    if type(article_ids) is str or type(article_ids) is int:
        article_ids = [article_ids]

    for id in article_ids:
        api_url = '{0}/account/articles/{1}'.format(environ['API_FIGSHARE_URL_BASE'], id)
        response = requests.get(api_url, headers=f.get_request_headers())
        if response.status_code == 200:
            article_info.append(json.loads(response.text))
        else:
            print('Error getting private article details for {0}, Response code {1}'.format(id, response.status_code))

    return article_info


def run(args):
    # Optionally writes a CSV report to file and returns a json array of objects with the data that was written.

    print('Getting institution articles')

    institution_articles = get_institution_articles()
    if institution_articles is None:
        print('Request Failed.')
        return []
    print("total number found: {0}".format(len(institution_articles)))

    print('Getting usage by public articles')
    public_articles = [item for item in institution_articles if item['published_date'] is not None]
    public_article_ids = []
    for article in public_articles:
        public_article_ids.append(article['id'])
    print("total public articles (including removed articles): {0}".format(len(public_article_ids)))

    public_articles_info = []
    unpublished_article_ids = []
    p = Pool(processes=5)
    result = p.map(get_public_article_info, public_article_ids)
    p.close()
    p.join()

    # unpack the list of pairs of return values and remove all the empty lists to get correct counts
    for r1, r2 in result:
        if len(r1) > 0:
            public_articles_info.append(r1)
        if len(r2) > 0:
            unpublished_article_ids.append(r2)

    print("total public articles (excluding removed articles): {0}".format(len(public_articles_info)))

    print('Getting usage by private articles')
    private_articles = [item for item in institution_articles if item['published_date'] is None]
    private_article_ids = []
    for article in private_articles:
        private_article_ids.append(article['id'])
    for article_id in unpublished_article_ids:
        private_article_ids.append(article_id)
    print("total private articles (including removed articles): {0}".format(len(private_article_ids)))

    private_articles_info = []
    p = Pool(processes=5)
    result = p.map(get_private_article_info, private_article_ids)
    p.close()
    p.join()

    for r in result:
        if len(r) > 0:
            private_articles_info.append(r)

    articles = []
    total_usage = 0
    for article in public_articles_info + private_articles_info:
        for article_version in article:
            articles.append({'id': article_version['id'], 'version': article_version['version'],
                             'totalfilesize': f.format_bytes(article_version['size'], args.units),
                             'title': article_version['title'],
                             'type': article_version['defined_type_name'],
                             'published_date': datetime.strptime(article_version['published_date'], "%Y-%m-%dT%H:%M:%SZ")
                             .strftime("%Y-%m-%d %H:%M:%S") if article_version['published_date'] else '',
                             'modified_date': datetime.strptime(article_version['modified_date'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
                             'embargo_date': article_version['embargo_date'] if article_version['embargo_date'] else '',
                             'embargo_type': article_version['embargo_type'] if article_version['embargo_type'] else '',
                             'embargo_options_type': article_version['embargo_options'][0]['type'] if article_version['embargo_options'] else '',
                             'is_embargoed': article_version['is_embargoed'],
                             'is_public': article_version['is_public'],
                             'report_date': f.get_report_date().strftime('%Y-%m-%d %H:%M:%S')
                             })
            total_usage += article_version['size']

    outfile = None
    if args.outfile:
        outfile = f.get_report_outfile(args.outfile, 'items')
        outfile.write(
            f'id,version,size ({args.units}),'
            + 'title,type,is_public,published (UTC),last_modified (UTC),embargo date (UTC),embargo type,embargo options,is embargoed,report date\n')
    else:
        print(f'id\t,version\t,size ({args.units})\t,title,type,published')

    for article in articles:
        if outfile:
            s = '{0},{1},{2},{3},{4},{11},{5},{6},{7},{8},{9},{10},{12}'
        else:
            s = '{0}\t,{1}\t,{2}\t,{3}\t,{4}\t,{5}'

        s = s.format(article['id'], article['version'], article['totalfilesize'],
                     '"' + article['title'].replace('"', '""') + '"',
                     article['type'],
                     article['published_date'], article['modified_date'], article['embargo_date'], article['embargo_type'],
                     article['embargo_options_type'], article['is_embargoed'], article['is_public'], article['report_date'])

        if outfile:
            outfile.write(s + '\n')
        elif not args.sync_to_dashboard:
            print(s)

    print(f'Totals (bytes):\t\t{total_usage}')
    print(f'Totals ({args.units}):\t\t{f.format_bytes(total_usage, args.units)}')

    if outfile:
        outfile.close()

    return articles
