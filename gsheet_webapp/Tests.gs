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
  }
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
  }
}

function testData_insertExists_curators(){
  return {
    "postData": {
      "contents": JSON.stringify(
        {
          "action":"insertupdate",
          "accesskey": PropertiesService.getScriptProperties().getProperty("accesskey"),
          "sheet": "curators",
          "data": 
              [
                {
                  "username": "hadepoju",
                  "id": "65a860d9a082cedfebebe8de",
                  "total_items": 3,
                  "total_time": 14707.716,
                  "easy_items": 1,
                  "easy_time": 938.044,
                  "med_items": 1,
                  "med_time": 1939.21,
                  "hard_items": 1,
                  "hard_time": 11830.462,
                  "3M_items": 3,
                  "3M_time": 14707.716,
                  "6M_items": 3,
                  "6M_time": 14707.716,
                  "1Y_items": 3,
                  "1Y_time": 14707.716,
                  "2Y_items": 3,
                  "2Y_time": 14707.716,
                  "3M_easy_items": 1,
                  "3M_easy_time": 938.044,
                  "3M_med_items": 1,
                  "3M_med_time": 1939.21,
                  "3M_hard_items": 1,
                  "3M_hard_time": 11830.462,
                  "6M_easy_items": 1,
                  "6M_easy_time": 938.044,
                  "6M_med_items": 1,
                  "6M_med_time": 1939.21,
                  "6M_hard_items": 1,
                  "6M_hard_time": 11830.462,
                  "1Y_easy_items": 1,
                  "1Y_easy_time": 938.044,
                  "1Y_med_items": 1,
                  "1Y_med_time": 1939.21,
                  "1Y_hard_items": 1,
                  "1Y_hard_time": 11830.462,
                  "2Y_easy_items": 1,
                  "2Y_easy_time": 938.044,
                  "2Y_med_items": 1,
                  "2Y_med_time": 1939.21,
                  "2Y_hard_items": 1,
                  "2Y_hard_time": 11830.462,
                  "total_reviewer1_items": 1,
                  "total_reviewer1_time": 11830.462,
                  "total_reviewer2_items": 2,
                  "total_reviewer2_time": 2877.254,
                  "easy_reviewer1_items": 0,
                  "easy_reviewer1_time": 0,
                  "easy_reviewer2_items": 1,
                  "easy_reviewer2_time": 938.044,
                  "med_reviewer1_items": 0,
                  "med_reviewer1_time": 0,
                  "med_reviewer2_items": 1,
                  "med_reviewer2_time": 1939.21,
                  "hard_reviewer1_items": 1,
                  "hard_reviewer1_time": 11830.462,
                  "hard_reviewer2_items": 0,
                  "hard_reviewer2_time": 0,
                  "3M_reviewer1_items": 1,
                  "3M_reviewer1_time": 11830.462,
                  "3M_reviewer2_items": 2,
                  "3M_reviewer2_time": 2877.254,
                  "6M_reviewer1_items": 1,
                  "6M_reviewer1_time": 11830.462,
                  "6M_reviewer2_items": 2,
                  "6M_reviewer2_time": 2877.254,
                  "1Y_reviewer1_items": 1,
                  "1Y_reviewer1_time": 11830.462,
                  "1Y_reviewer2_items": 2,
                  "1Y_reviewer2_time": 2877.254,
                  "2Y_reviewer1_items": 1,
                  "2Y_reviewer1_time": 11830.462,
                  "2Y_reviewer2_items": 2,
                  "2Y_reviewer2_time": 2877.254,
                  "3M_easy_reviewer1_items": 0,
                  "3M_easy_reviewer1_time": 0,
                  "3M_easy_reviewer2_items": 1,
                  "3M_easy_reviewer2_time": 938.044,
                  "6M_easy_reviewer1_items": 0,
                  "6M_easy_reviewer1_time": 0,
                  "6M_easy_reviewer2_items": 1,
                  "6M_easy_reviewer2_time": 938.044,
                  "1Y_easy_reviewer1_items": 0,
                  "1Y_easy_reviewer1_time": 0,
                  "1Y_easy_reviewer2_items": 1,
                  "1Y_easy_reviewer2_time": 938.044,
                  "2Y_easy_reviewer1_items": 0,
                  "2Y_easy_reviewer1_time": 0,
                  "2Y_easy_reviewer2_items": 1,
                  "2Y_easy_reviewer2_time": 938.044,
                  "3M_med_reviewer1_items": 0,
                  "3M_med_reviewer1_time": 0,
                  "3M_med_reviewer2_items": 1,
                  "3M_med_reviewer2_time": 1939.21,
                  "6M_med_reviewer1_items": 0,
                  "6M_med_reviewer1_time": 0,
                  "6M_med_reviewer2_items": 1,
                  "6M_med_reviewer2_time": 1939.21,
                  "1Y_med_reviewer1_items": 0,
                  "1Y_med_reviewer1_time": 0,
                  "1Y_med_reviewer2_items": 1,
                  "1Y_med_reviewer2_time": 1939.21,
                  "2Y_med_reviewer1_items": 0,
                  "2Y_med_reviewer1_time": 0,
                  "2Y_med_reviewer2_items": 1,
                  "2Y_med_reviewer2_time": 1939.21,
                  "3M_hard_reviewer1_items": 1,
                  "3M_hard_reviewer1_time": 11830.462,
                  "3M_hard_reviewer2_items": 0,
                  "3M_hard_reviewer2_time": 0,
                  "6M_hard_reviewer1_items": 1,
                  "6M_hard_reviewer1_time": 11830.462,
                  "6M_hard_reviewer2_items": 0,
                  "6M_hard_reviewer2_time": 0,
                  "1Y_hard_reviewer1_items": 1,
                  "1Y_hard_reviewer1_time": 11830.462,
                  "1Y_hard_reviewer2_items": 0,
                  "1Y_hard_reviewer2_time": 0,
                  "2Y_hard_reviewer1_items": 1,
                  "2Y_hard_reviewer1_time": 11830.462,
                  "2Y_hard_reviewer2_items": 0,
                  "2Y_hard_reviewer2_time": 0
                }
              ]
        }
      )
    }
  }
}