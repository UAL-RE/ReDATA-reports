# Copy this file as secrets.py and replace the values with your own.
# Do not commit secrets.py to version control.
# Use secrets.py to store secrets so code works locally and as a DO function (see project.yml).

# Figshare API
api_figshare_url_base = ''
api_figshare_token = ''

# Trello API
api_trello_url_base = ''
api_trello_key = ''
api_trello_token = ''
trello_board_id = ''

# Google sheet
gsheets_dashboard_post_url = ''
gsheets_dashboard_key = ''

# DO access token. When deployed as a function, all requests must send this token in the 't' parameter of the GET request
do_token = ''

# static mapping of ids for deleted users (see readme). Userids are usually lower case
deleted_users = {'user1':'id1',
                 'user2':'id2'
                }