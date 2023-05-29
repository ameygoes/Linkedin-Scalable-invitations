TEST_DB_NAME = "linkedin_automation_test"
PRD_DB_NAME = "linkedin_automation"

PROFILE_TABLE_TEST = "profile_test"
PROFILE_TABLE = "profile"

PROFILE_TABLE_COLUMNS = ['public_id','profile_urn_id', 'profile_firstName','profile_lastName','profile_network_distance','profile_latest_company','profile_latest_job_title','category', 'connection_req_withdrawn_status','connection_req_withdrawn_date','record_added_to_sheet']
NO_UPDATE_COLS = ['category', 'connection_req_withdrawn_status','connection_req_withdrawn_date','record_added_to_sheet']