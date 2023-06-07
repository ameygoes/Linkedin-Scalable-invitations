CREATE DATABASE IF NOT EXISTS EMAIL_JOBS;
USE EMAIL_JOBS;

CREATE TABLE IF NOT EXISTS linkedin_automation_profile (
    public_id VARCHAR(255),
    profile_urn_id VARCHAR(255),
    profile_firstName VARCHAR(255),
    profile_lastName VARCHAR(255),
    profile_network_distance INT,
    profile_latest_company VARCHAR(255),
    profile_latest_job_title VARCHAR(255),
    category VARCHAR(255),
    connection_req_sent_status BOOLEAN,
    connection_req_sent_date VARCHAR(15),
    connection_req_withdrawn_status BOOLEAN,
    connection_req_withdrawn_date VARCHAR(15),
    record_added_to_db VARCHAR(15),
    PRIMARY KEY (profile_urn_id)
);

CREATE TABLE IF NOT EXISTS linkedin_automation_profile_test (
    public_id VARCHAR(255),
    profile_urn_id VARCHAR(255),
    profile_firstName VARCHAR(255),
    profile_lastName VARCHAR(255),
    profile_network_distance INT,
    profile_latest_company VARCHAR(255),
    profile_latest_job_title VARCHAR(255),
    category VARCHAR(255),
    connection_req_sent_status BOOLEAN DEFAULT false,
    connection_req_sent_date VARCHAR(15),
    connection_req_withdrawn_status BOOLEAN DEFAULT false,
    connection_req_withdrawn_date VARCHAR(15),
    record_added_to_db VARCHAR(15),
    PRIMARY KEY (profile_urn_id)
);
