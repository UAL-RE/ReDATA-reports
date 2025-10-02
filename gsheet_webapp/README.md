# Google Sheets WebApp

This Sheet accepts data from the report generator via a POST and stores it for use by the LookerStudio dashboard.

## Sheet Setup

1. Create a new Google Sheet document in the same Google account as the LookerStudio dashboard
1. Add the following sheets
	1. `Readme` (optional)
	1. `items`. Create columns exactly matching the name and order of the keys in the `articles` dictionary from [`items_report.py`](../packages/redata_reports/run/items_report.py)
	1. `users`. Create columns exactly matching the name and order of the keys in the `account_info` dictionary from [`userquota_report.py`](../packages/redata_reports/run/userquota_report.py)
	1. `curators`. Create columns exactly matching the name and order of the `curators` dictionary from [`curators_report.py`](../packages/trello_reports/run/curators_report.py)
	1. `curators-timeunpivot`. See [Data Transformation Setup](#data-transformation).
	1. `curators-itemunpivot`. See [Data Transformation Setup](#data-transformation).

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

# Data Transformation

Additional data transformation is required for some datasets for use in LookerStudio. Namely, the data from the `curators` sheet.

## Setup

Add the data manipulation script
1. Go to Extensions -> Apps Script
1. Create a new file `Unpivot.gs` and copy the contents of the corresponding file in this repo to it.

Create the following formulas
In `curators-timeunpivot`, in cell A1 enter, the following formula
```
=unpivot({curators!A1:A30,curators!D1:D30,curators!F1:F30,curators!H1:H30,curators!J1:J30,curators!L1:L30,curators!N1:N30,curators!P1:P30,curators!R1:R30,curators!T1:T30,curators!V1:V30,curators!X1:X30,curators!Z1:Z30,curators!AB1:AB30,curators!AD1:AD30,curators!AF1:AF30,curators!AH1:AH30,curators!AJ1:AJ30,curators!AL1:AL30,curators!AN1:AN30,curators!AP1:AP30,curators!AR1:AR30,curators!AT1:AT30,curators!AV1:AV30,curators!AX1:AX30,curators!AZ1:AZ30,curators!BB1:BB30,curators!BD1:BD30,curators!BF1:BF30,curators!BH1:BH30,curators!BJ1:BJ30,curators!BL1:BL30,curators!BN1:BN30,curators!BP1:BP30,curators!BR1:BR30,curators!BT1:BT30,curators!BV1:BV30,curators!BX1:BX30,curators!BZ1:BZ30,curators!CB1:CB30,curators!CD1:CD30,curators!CF1:CF30,curators!CH1:CH30,curators!CJ1:CJ30,curators!CL1:CL30,curators!CN1:CN30,curators!CP1:CP30,curators!CR1:CR30,curators!CT1:CT30,curators!CV1:CV30,curators!CX1:CX30,curators!CZ1:CZ30,curators!DB1:DB30,curators!DD1:DD30,curators!DF1:DF30},1,1,"time_category","time")
```

In `curators-itemunpivot` in cell A1, enter the following formula
```
=unpivot({curators!A1:A30,curators!C1:C30,curators!E1:E30,curators!G1:G30,curators!I1:I30,curators!K1:K30,curators!M1:M30,curators!O1:O30,curators!Q1:Q30,curators!S1:S30,curators!U1:U30,curators!W1:W30,curators!Y1:Y30,curators!AA1:AA30,curators!AC1:AC30,curators!AE1:AE30,curators!AG1:AG30,curators!AI1:AI30,curators!AK1:AK30,curators!AM1:AM30,curators!AO1:AO30,curators!AQ1:AQ30,curators!AS1:AS30,curators!AU1:AU30,curators!AW1:AW30,curators!AY1:AY30,curators!BA1:BA30,curators!BC1:BC30,curators!BE1:BE30,curators!BG1:BG30,curators!BI1:BI30,curators!BK1:BK30,curators!BM1:BM30,curators!BO1:BO30,curators!BQ1:BQ30,curators!BS1:BS30,curators!BU1:BU30,curators!BW1:BW30,curators!BY1:BY30,curators!CA1:CA30,curators!CC1:CC30,curators!CE1:CE30,curators!CG1:CG30,curators!CI1:CI30,curators!CK1:CK30,curators!CM1:CM30,curators!CO1:CO30,curators!CQ1:CQ30,curators!CS1:CS30,curators!CU1:CU30,curators!CW1:CW30,curators!CY1:CY30,curators!DA1:DA30,curators!DC1:DC30,curators!DE1:DE30},1,1,"item_category","count")
```