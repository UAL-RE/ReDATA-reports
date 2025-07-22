# Copy this file as secrets.py and replace the values with your own.
# Do not commit secrets.py to version control.
# Use secrets.py to store secrets so code works locally and as a DO function (see project.yml).

from os import environ

# Figshare API
api_figshare_url_base = ''
api_figshare_token = ''

# Trello API
api_trello_url_base = ''
api_trello_key = ''
api_trello_token = ''
trello_board_id = ''
trello_publishedlist_id = ''

# Google sheet
gsheets_dashboard_post_url = ''
gsheets_dashboard_key = ''

# DO access token. When deployed as a function, all requests must send this token in the 't' parameter of the GET request
do_token = ''
