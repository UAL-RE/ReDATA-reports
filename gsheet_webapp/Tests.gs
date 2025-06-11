function testData_insertActionOnly() {
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("accesskey"),
          "sheet": "items"
        }
      )
    }
  };
}

function testData_insertExists_items(){
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("accesskey"),
          "sheet": "items",
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

function testData_insertExists_users(){
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("accesskey"),
          "sheet": "users",
          "data": 
              [
                {
                  "created_date": "2020-02-20T10:21:28Z",
                  "modified_date": "2021-10-11T16:40:11Z",
                  "group_id": 26114,
                  "quota": 1073741824,
                  "maximum_file_size": 0,
                  "used_quota": 0,
                  "used_quota_private": 0,
                  "used_quota_public": 0,
                  "pending_quota_request": false,
                  "id": 2267819,
                  "first_name": "ReDATA",
                  "last_name": "Administrator",
                  "email": "data-management@arizona.edu",
                  "active": 1,
                  "institution_id": 797,
                  "institution_user_id": "",
                  "user_id": 8472170,
                  "orcid_id": "",
                  "report_date": "2025-06-11 14:46:27"
                }
              ]
          }
      )
    }
  };
}
