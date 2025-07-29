# Report Data Generator

Collects data from ReDATA that can be used to create reports. Data is output in CSV format.

- Items report: Information about public and private items and their versions. Note this report overestimates the total storage used because it does take into account the fact that Figshare does not make copies of unchanged files across dataset versions. The users report is the most accurate way to get total storage used.
- Users report: Information about user accounts

The project is structured as a Digital Ocean Function but can be executed independently as well. The code should work with any Figshare for Institutions instance. 

# Local Usage

Install
```
pip install -r ./packages/redata_reports/run/requirements.txt
```

Show the command line options by running
```
python ./packages/redata_reports/run/main.py -h
```

or
```
python ./packages/trello_reports/run/main.py -h
```

Prior to generating any reports, configure API endpoints and keys. Copy [`./lib/secrets.example.py`](lib/secrets.example.py) to `./lib/secrets.py` and edit the fields with the appropriate values. See the comments in that file for specific instructions. To generate reports locally, Google Sheets and DigitalOcean credentials are not needed.

Generate a report. E.g the users report. A CSV will be output in the current working directory in this example.
```
python ./packages/redata_reports/run/main.py -r users -o
```

## Dashboard

The `--sync-to-dashboard` option uploads data to the Google dashboard (data is stored in a Google Sheet and displayed in a Looker Studio dashboard). Setting this flag includes `-u B -r items -r users`. The destination sheet is configured in `secrets.py`. 

Prior to using `--sync-to-dashboard`, the target Google Sheet must be set up. See the [readme](gsheet_webapp/README.md) in `gsheet_webapp`. Once that is done, run (for example):
```
python packages/redata_reports/main.py --sync-to-dashboard
```
A `data.json` file is auto-generated in the current working directory. This file can be deleted once the sync completes.


### Testing the sheet upload endpoint using cURL:

Call the webapp in the sheet, replacing XXXXX and YYYYY with the appropriate values

Simple test (no data uploaded):
```
curl -L "https://script.google.com/macros/s/XXXXXXXX/exec" -H "Content-Type: application/json"  --data '{"action":"insertupdate","accesskey":"YYYYYY"}'
```

With data upload:
```
curl -L "https://script.google.com/macros/s/XXXXXXXX/exec" -H "Content-Type: application/json" --data-binary @data.json
```

### Example Dashboard
An example of how the data can be presented/summarized in a dashboard using LookerStudio.
<details>
  <summary>Screenshot</summary>
  
  ![LookerStudioSample](https://github.com/user-attachments/assets/659abeb3-8a81-4eb6-8bb1-0632f50d8958)
  
</details>


## DO Functions

Authenticate to DO with `doctl` and connect to the desired functions namespace. The connect command will let you pick from a list if there is more than one functions namespace defined in the DO Functions console.
```
doctl serverless connect
```

Then deploy with
```
./deploy.sh
```

Once deployed, the function can be manually run which will call the equivalent of `main.py --sync-to-dashboard`. The URL of the function can be obtained from the Settings tab for the function in the DO console.
```
curl -X GET "https://<do url>/redata_reports/run?t=<token>" -H "Content-Type: application/json"
```

If automatic triggering is desired, the trigger should be configured manually in the DO console.
