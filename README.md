# Report Data Generator

Collects data from ReDATA that can be used to create reports. Data is output in CSV format.

- Items report: Information about public and private items and their versions
- Users report: Information about user accounts

The project is structured as a Digital Ocean Function but can be executed independently as well.

# Installation
```
pip install -r ./packages/redata_reports/run/requirements.txt
```

## Execution

Show the command line options by running

```
python ./packages/redata_reports/run/main.py -h
```

Prior to generating any reports, configure API endpoints and keys. Copy `secrets.example.py` to `secrets.py` and edit the fields with the appropriate values. 

## Dashboard

The `--sync-to-dashboard` option uploads data to the Google dashboard (data is stored in a Google Sheet and displayed in a Looker Studio dashboard). The flag is equivalent to the flags `-u B -r items -r users`. The destination sheet is configured in `secrets.py`.

```
python packages/redata_reports/main.py --sync-to-dashboard
```

### Testing the sheet upload endpoint using cURL:
Call the webapp in the sheet, replacing XXXXX and YYYYY with the appropriate values

Simple test - no data uploaded:

```
curl -L "https://script.google.com/macros/s/XXXXXXXX/exec" -H "Content-Type: application/json"  --data '{"action":"insertupdate","accesskey":"YYYYYY"}'
```

With data upload (data.json is generated when `--sync-to-dashboard` is set):

```
curl -L "https://script.google.com/macros/s/XXXXXXXX/exec" -H "Content-Type: application/json" --data-binary @data.json
```

## DO Functions
Authenticate to DO with `doctl` and connect to the desired functions namespace. The connect command will let you pick from a list if there is more than one functions namespace defined in the DO functions console.
```
doctl serverless connect
```

Then deploy with
```
./deploy.sh
```

Run the function which will call the equivalent of `main.py --sync-to-dashboard'
```
curl -X GET "https://<do url>/redata_reports/run?t=<token>" -H "Content-Type: application/json"
```
