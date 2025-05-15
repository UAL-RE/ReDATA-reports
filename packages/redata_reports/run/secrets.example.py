# Copy this file as secrets.py and replace the values with your own. 
# Do not commit secrets.py to version control.
# Use secrets.py to store secrets so code works locally and as a DO function (see project.yml).

# Figshare API
api_url_base = ''
api_token = ''

# Google sheet
gsheets_dashboard_post_url = ''
gsheets_dashboard_key = ''

# DO access token. When deployed as a function, all requests must send this token in the 't' parameter of the GET request
do_token = ''


# **************************************************************
from os import environ
environ['API_URL_BASE'] = api_url_base
environ['API_TOKEN'] = api_token
environ['GSHEETS_DASHBOARD_POST_URL'] = gsheets_dashboard_post_url
environ['GSHEETS_DASHBOARD_KEY'] = gsheets_dashboard_key
environ['TOKEN'] = do_token