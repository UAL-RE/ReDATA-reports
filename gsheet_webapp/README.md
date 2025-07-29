# Google Sheets WebApp

This Sheet accepts data from the report generator via a POST and stores it for use by the LookerStudio dashboard.

## Sheet Setup

1. Create a new Google Sheet document in the same Google account as the LookerStudio dashboard
1. Add the following sheets
	1. `Readme` (optional)
	1. `items`. Create columns exactly matching the name and order of the keys in the `articles` dictionary from [`items_report.py`](../packages/redata_reports/run/items_report.py)
	1. `users`. Create columns exactly matching the name and order of the keys in the `account_info` dictionary from [`userquota_report.py`](../packages/redata_reports/run/userquota_report.py)
	1. `curators`. Create columns exactly matching the name and order of the `curators` dictionary from [`curators_report.py`](../packages/trello_reports/run/curators_report.py)

## WebApp

### Setup

1. Go to Extensions -> Apps Script
1. Create new files in the Apps Script matching the names of the .gs files in this directory
1. Ensure that the files in the Apps Script are exactly in this order from top to bottom
	1. `HTTPMessages.gs`
	1. `Tests.gs`
	1. `Code.gs` 
1. Copy the contents of each file to the corresponding file in the Apps Script
1. Add the [BetterLog](https://github.com/peterherrmann/BetterLog) library for logging
	1. Click on the + beside Libraries in the sidebar
	1. Paste the script id `1DSyxam1ceq72bMHsE6aOVeOl94X78WCwiYPytKi7chlg4x5GqiNXSw0l`
	1. Click Look Up and then Add.
1. Create the auth token
	1. Open the project settings by clicking the gear icon on the left
	1. Under Script Properties, add a new property `accesskey`
	1. Set the value to be the same as `gsheets_dashboard_key` in [`secrets.py`](../packages/redata_reports/run/secrets.example.py)
	
### Deployment

1. From the Apps Script code editor, run the `setup` function.
1. Deploy the WebApp
	1. Click Deploy -> New Deployment
	1. Select a WebApp deployment
	1. When prompted, set the security level to execute as "me" and access to "anyone, even anonymously" and enable service
	1. Copy the URL of the deployed app to `gsheets_dashboard_post_url` in [`secrets.py`](packages/redata_reports/run/secrets.example.py)
	
### Testing

1. See the `test` function in `Code.gs`

### Updating

Manually copy any changes in this repo to the appropriate files in Apps Script.

To deploy the update and keep the app URL the same:

1. Deploy -> Manage deployments -> pencil icon -> Version dropdown -> New Version -> Deploy

Note: a new version is always required, you can't update an existing version.