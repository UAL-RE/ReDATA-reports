function testData_insertActionOnly() {
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("key")
        }
      )
    }
  };
}

function testData_insertExists(){
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("key"),
          "data": 
              [
                {
                  "id": 28647359,
                  "version": 1,
                  "totalfilesize": "65657485",
                  "title": "Tomopac2: an unfolded-slab plate reconstruction validated via mantle circulation models in a closed-loop experiment",
                  "type": "dataset",
                  "published_date": "2025-03-29 00:54:39",
                  "modified_date": "2025-03-29 00:54:39",
                  "embargo_date": "",
                  "embargo_type": "",
                  "embargo_options_type": "",
                  "is_embargoed": false,
                  "is_public": true,
                  "report_date": "2025-04-03 20:37:32"
                }, {
                  "id": 28642256,
                  "version": 1,
                  "totalfilesize": "108181954",
                  "title": "Data and Stata code for Climate Shocks and Human Capital: Evidence from Uganda Paper",
                  "type": "dataset",
                  "published_date": "2025-04-03 22:50:07",
                  "modified_date": "2025-04-03 22:50:07",
                  "embargo_date": "",
                  "embargo_type": "",
                  "embargo_options_type": "",
                  "is_embargoed": false,
                  "is_public": true,
                  "report_date": "2025-04-03 20:37:32"
                }
              ]
          }
      )
    }
  };
}
