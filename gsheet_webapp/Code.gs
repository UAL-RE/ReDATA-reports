// https://mashe.hawksey.info/2014/07/google-sheets-as-a-database-insert-with-apps-script-using-postget-methods-with-ajax-example/

/*        
    1. Run function > setup

    2. Deploy as web app 
      - Deploy -> New Deployment
      - set security level and enable service (most likely execute as 'me' and access 'anyone, even anonymously) 
    2a. Updating
      - Deploy -> Manage deployments -> pencil icon -> versions -> New Version -> Deploy

    3. Copy the 'Current web app URL' and post this in your form/script action 

    4. Insert column names on your destination sheet matching the parameter names of the data you are passing in (exactly matching case)
*/

var SCRIPT_PROP = PropertiesService.getScriptProperties(); // new property service

version="2.0.0"; //change when the version changes

//Best practice for using BetterLog and logging to a spreadsheet:
// You can add and set the property "BetterLogLevel" in File > Project Properties and change it to
// "OFF","SEVERE","WARNING","INFO","CONFIG","FINE","FINER","FINEST" or "ALL" at runtime without editing code.
Logger = BetterLog.setLevel(); //defaults to 'INFO' level
Logger.useSpreadsheet(SpreadsheetApp.getActiveSpreadsheet().getId());

Logger.info('ReDATA Reporting Data v' + version);

function test(){
  /* See here when testing POST with cURL to avoid "Sorry, unable to open the file at this time."
  https://stackoverflow.com/questions/49618265#comment113436606_49618605
  I.e., omit -X POST:
    curl -L "script url" -H "Content-Type: application/json"  --data '{"action":"insertupdate"}'
  */

  //e=testData_insertExists_users();
  //e=testData_insertExists_items();
  e=testData_insertExists_curators();
  
  console.log(doPost(e).getContent());
}

// If you don't want to expose either GET or POST methods you can comment out the appropriate function
function doGet(e){
  return ContentService.createTextOutput("ok");
}

function doPost(e){
  /* 
  function accepts only json.
  JSON must contain at least 1 key called 'action'
  */
  var jsonString;
  var action;
  var result = result_ok;

  //Logger.info(e.postData.contents);

  jsonString = e.postData.contents;
  try{
    objJSON = JSON.parse(jsonString);
    action = objJSON.action;
    key = objJSON.accesskey;
    
    if(key != SCRIPT_PROP.getProperty("accesskey"))
      throw new Error("Invalid access key.");

    Logger.info(action);
    
    result = handleAction(action, objJSON);

  } catch(err){
    result = {"result":"error", "error": err.message};
  }

  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
}

function handleAction(action, objJSON) {
  var result = result_ok;
  var data = objJSON.data;
  var sheet = objJSON.sheet;
  try {
    switch(action) {
      case "readall":
        break;
      case "insertupdate":
        result = insert_or_update(data, sheet);
        break;
      default:
        result = result_forbidden;
    }
  } catch (e) { //with stack tracing if your exceptions bubble up to here
    e = (typeof e === 'string') ? new Error(e) : e;
    e = (typeof e === 'string') ? new Error(e) : e;
    result = result_error;
  }
  return result;
}

function insert_or_update(data, sheet_name, headRow = 1) {
  /*
  See Tests for the expected data format
  */

  // we want a public lock, one that locks for all invocations
  var lock = LockService.getPublicLock();
  lock.waitLock(30000);  // wait 30 seconds before conceding defeat.

  try {
    // next set where we write the data - you could write to multiple/alternate destinations
    var doc = SpreadsheetApp.openById(SCRIPT_PROP.getProperty("spreadsheet_id"));
    var sheet = doc.getSheetByName(sheet_name);

    var headers = sheet.getRange(headRow, 1, 1, sheet.getLastColumn()).getValues()[0];
    var numRowsBeforeUpdate = sheet.getLastRow();
    var numRowsAfterUpdate = numRowsBeforeUpdate;
    var rows = [];
    for (item of data){
      var row = [];

      // loop through the header columns
      for (i in headers){
        if (headers[i] == "Timestamp"){ // special case if you include a 'Timestamp' column
          row.push(new Date());
        } else { // else use header name to get data
          row.push(item[headers[i].trim()]);
        }
      }
      rows.push(row);
    }

    // clear sheet before adding values
    if(sheet.getLastRow()>1){
      sheet.deleteRows(2, sheet.getLastRow()-1);
    }

    // more efficient to set values as [][] array than individually
    sheet.getRange(sheet.getLastRow()+1, 1, rows.length, rows[0].length).setValues(rows);

    SpreadsheetApp.flush();
    numRowsAfterUpdate = sheet.getLastRow();

    // return json success results
    Logger.info("Success, rows added or changed: " + (numRowsAfterUpdate - numRowsBeforeUpdate));
    return {"result":"success", "rows_addedchanged": (numRowsAfterUpdate - numRowsBeforeUpdate)};

  } catch(e){
    Logger.severe(e);
    // if error return this
    return {"result":"error", "error": e.message};
  } finally { //release lock
    lock.releaseLock();
  }
  
}

function setup() {
    var doc = SpreadsheetApp.getActiveSpreadsheet();
    SCRIPT_PROP.setProperty("spreadsheet_id", doc.getId());
}
