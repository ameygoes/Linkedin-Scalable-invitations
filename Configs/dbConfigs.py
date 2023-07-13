import os

# depricated
PROFILE_TABLE_COLUMNS = ['public_id','profile_urn_id', 'profile_firstName','profile_lastName','profile_network_distance','profile_latest_company','profile_latest_job_title','category', 'connection_req_sent_status','connection_req_sent_date', 'connection_req_withdrawn_status','connection_req_withdrawn_date','record_added_to_db']
NO_UPDATE_COLS = ['category', 'connection_req_sent_status','connection_req_sent_date', 'connection_req_withdrawn_status','connection_req_withdrawn_date','record_added_to_db']


DB_USER_NAME = "EMAIL_HR"
DB_PASSWORD = os.environ.get("EMAIL_HR_DB_PASS")
HOST_NAME = "localhost"
DB_NAME = "EMAIL_JOBS"
PORT_NAME = "3306"
PROD_TABLE_NAME = "linkedin_automation_profile"
TEST_TABLE_NAME = "linkedin_automation_profile_test"

# Prepare the SQL query with placeholders for multiple profile URN IDs
CHECK_IF_EXISTS_IN_BULK = "SELECT profile_urn_id FROM {} WHERE profile_urn_id IN ({})"


SEARCH_QUERY = "SELECT count(*) FROM {} WHERE profile_urn_id = '{}'"
CHECK_DB = "SHOW DATABASES LIKE '{}'"
CHECK_TABLE = "SHOW TABLES LIKE '{}'"
INSERT_QUERY = "INSERT INTO {} VALUES('{}', '{}', '{}', '{}', {}, {}, '{}', {}, {})"
CHECK_IF_EXISTS =  "SELECT COUNT(*) FROM {} WHERE `profile_urn_id` = %s"
INSERT_QUERY_PROFILE = "INSERT INTO {} (`public_id`, `profile_urn_id`, `profile_firstName`, `profile_lastName`, `profile_network_distance`, `profile_latest_company`, `profile_latest_job_title`, `category`, `connection_req_sent_status`, `connection_req_sent_date`, `connection_req_withdrawn_status`, `connection_req_withdrawn_date`, `record_added_to_db`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
UPDATE_QUERY_STR = "UPDATE {} SET {} = '{}' WHERE profile_urn_id = '{}'"
UPDATE_QUERY_NON_STR = "UPDATE {} SET {} = {} WHERE profile_urn_id = '{}'"
TRUNCATE_TABLE = "TRUNCATE TABLE {}"
CHECK_IF_EMAIL_SENT_BEFORE = "SELECT COUNT(*) FROM {} WHERE EMAIL=`{}`"
UPDATE_CONN_REQ_STATUS = "connection_req_sent_status"
UPDATE_CONN_REQ_DATE = "connection_req_sent_date"
UPDATE_CONN_REQ_WITHDRAWN_STATUS = "connection_req_withdrawn_status"
UPDATE_CONN_REQ_WITHDRAWN_DATE = "connection_req_withdrawn_date"
UPDATE_COL_5 = ""

FETCH_COMPANY_PEOPLE_FOR_OFFSET = "SELECT count(profile_urn_id) FROM {} WHERE `profile_latest_company` = '{}' AND category = '{}'"
FETCH_COMPANY_PEOPLE = "SELECT * FROM {} WHERE `profile_latest_company` = '{}' AND category = '{}'"

FETCH_COMPANY_RECRUITERS = "SELECT * FROM {} WHERE `profile_latest_company` = '{}' AND category = 'hr'"
FETCH_RECRUITERS_BELONGING_TO_A_COMPANY_TO_WHOM_FRIEND_REQ_NOT_SENT = "SELECT profile_urn_id, profile_firstName, profile_lastName FROM {} WHERE `profile_latest_company` = '{}' AND category = 'hr' AND connection_req_sent_status = False"
FETCH_ALL_RECRUITERS_TO_WHOM_FRIEND_REQ_NOT_SENT = "SELECT profile_urn_id, profile_firstName, profile_lastName FROM {} WHERE category = 'hr' AND connection_req_sent_status = False"

FETCH_PEOPLE_CONN_WITHDRWAN_3_WEEKS_AGO = "SELECT profile_urn_id FROM {} WHERE connection_req_withdrawn_date < DATE_SUB(NOW(), INTERVAL 3 WEEK)" 

FETCH_COMPANY_RECRUITERS_FOR_OFFSET = "SELECT count(profile_urn_id) FROM {} WHERE `profile_latest_company` = '{}' AND category = '{}'"
FETCH_DATA_ENGG_BELONGING_TO_A_COMPANY_TO_WHOM_FRIEND_REQ_NOT_SENT = "SELECT profile_urn_id, profile_firstName, profile_lastName FROM {} WHERE `profile_latest_company` = '{}' AND category = 'data' AND connection_req_sent_status = False"
FETCH_ALL_DATA_ENGG_TO_WHOM_FRIEND_REQ_NOT_SENT = "SELECT profile_urn_id, profile_firstName, profile_lastName FROM {} WHERE category = 'data' AND connection_req_sent_status = False"