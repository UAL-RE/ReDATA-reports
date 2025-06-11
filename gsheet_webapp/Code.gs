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

version="1.1"; //change when the version changes

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

  e=testData_insertExists_users();
  //e=testData_insertExists_items();
  
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
          row.push(item[headers[i]]);
        }
      }
      rows.push(row);
    }

    // more efficient to set values as [][] array than individually
    sheet.getRange(sheet.getLastRow()+1, 1, rows.length, rows[0].length).setValues(rows);

    dedupe(sheet, headers);
    numRowsAfterUpdate = sheet.getLastRow();

    // return json success results
    Logger.info("Success, rows added: " + (numRowsAfterUpdate - numRowsBeforeUpdate));
    return {"result":"success", "rows_added": (numRowsAfterUpdate - numRowsBeforeUpdate)};

  } catch(e){
    Logger.severe(e);
    // if error return this
    return {"result":"error", "error": e.message};
  } finally { //release lock
    lock.releaseLock();
  }
  
}

function dedupe(sheet, headers) {
    /*
    Remove duplicates from the given sheet based on specific criteria.
    */

    var alldata;
    var reportDateCol = 0;
    
    // get the index of the report_date column
    for (i in headers){
        if (headers[i] == "report_date"){
          reportDateCol = parseInt(i) + 1;
          break;
        }
    }

    //skip the header
    alldata = sheet.getRange(2, 1, sheet.getLastRow(), sheet.getLastColumn());

    switch(sheet.getName()) {
      case "items":
        // Remove any duplicates based on id, version. This will still overestimate storage use slightly since it doesn't
        // take into account the fact that figshare does not duplicate unchanged files across dataset versions.
        // The user report is actually the more accurate storage measure
        alldata.removeDuplicates([1, 2]);
        break;
      case "users":
        //first, remove exact duplicates (i.e., where none of the information changed)
        alldata.removeDuplicates([1, 2, 3, 4, 5, 6, 7]);
        
        // When any information changes, keep the latest version of the record only.
        // Reverse sort the range by report date so that removeDuplicates removes the earlier entry, keeping the latest one.
        alldata.sort({column: reportDateCol, ascending: false});
        
        // Now, remove duplicates based on email only. The total number of items should be equal to the total number of user accounts + 1
        alldata.removeDuplicates([1]);
        
        //sort ascending again
        alldata.sort({column: reportDateCol, ascending: true});
        
        break;
      default:
        throw new Error("Sheet " + sheet_name + " not found for dedupe");
    }

}

function setup() {
    var doc = SpreadsheetApp.getActiveSpreadsheet();
    SCRIPT_PROP.setProperty("spreadsheet_id", doc.getId());
}
