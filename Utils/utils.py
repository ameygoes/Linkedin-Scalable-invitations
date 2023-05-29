from datetime import datetime
import json
import os
import pandas as pd
from Configs.envrinomentSpecificConfgis import CACHE_FILE
from Configs.jobConfigs import FIRSTNAME, LASTNAME, PUBLIC_PROFILE_ID
from fuzzywuzzy import fuzz


def getCurrentTime():
    return datetime.now()

def getCurrentDate():

    # Get the current date
    today = datetime.now().date()

    # Format the date as "dd-mm-yyyy"
    formatted_date = today.strftime("%d-%m-%Y")

    return formatted_date

def getTotalTime(totalSeconds):
    hours = int(totalSeconds // 3600)
    minutes = int((totalSeconds % 3600) // 60)
    seconds = int(totalSeconds % 60)
    return hours, minutes, seconds

def writeJSONfile(filepath, data):
    # Write the JSON object to a file.
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def readJSONfile(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def get_id_from_urn(urn):
    return urn.split(":")[3]

def cache_public_profile_id(api):

    """
    Caches the public profile id of the logged in user.
    """

    # Check if the file exists.
    if os.path.isfile(CACHE_FILE):

        # Get the size of the file.
        file_size = os.path.getsize(CACHE_FILE)

        # Check if the file is empty.
        if file_size == 0:
            # Write the profile to the file.
            writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

        # Read the profile from the file.
        cache_profile = readJSONfile(CACHE_FILE)

        # Check if the profile is up-to-date.
        if cache_profile["firstName"] == FIRSTNAME and cache_profile["lastName"] == LASTNAME:
            return cache_profile

        # The profile is not up-to-date, so write the new profile to the file.
        writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

        return readJSONfile(CACHE_FILE)

    # The file does not exist, so write the profile to the file.
    writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

    return readJSONfile(CACHE_FILE)

def getProfileCategory(job_title):
    

    job_titles = ['Recruiter', 'Technical Recruiter', 'Talent Acquisition Specialist', 'Talent Acquisition Partner', 'Recruitment Specialist', 'Recruitment Consultant', 'Talent Sourcer', 'Staffing Specialist', 'HR Recruiter', 'Hiring Specialist', 'Recruitment Coordinator', 'Recruitment Manager', 'Talent Scout', 'Headhunter', 'Recruitment Executive', 'Talent Acquisition Manager', 'Recruitment Team Lead', 'Recruitment Associate', 'Sourcing Specialist', 'Talent Acquisition Coordinator', 'Recruitment Lead', 'Recruitment Analyst', 'Senior Technical Recruiter', 'Junior Recruiter', 'Recruitment Operations Specialist', 'Corporate Recruiter', 'Campus Recruiter', 'Employment Specialist', 'RPO Recruiter', 'Recruitment Business Partner']

    # Threshold for matching percentage (70% in this example)
    match_threshold = 70

    # Check if the jobTitle partially matches any job title from the list
    matches = [title for title in job_title if fuzz.partial_ratio(job_title.lower(), title.lower()) >= match_threshold]

    # If there are any matches, assign the category "HR"
    category = "HR" if matches else "DEV"

    # print("Matches:", matches)
    # print("Category:", category)
    return category

def checkIfKeyExists(response, key_to_check):
    if key_to_check in response:
        return response[key_to_check]
    return None

def get_df_items_for_search_results(profile):
    return {'public_id': profile.public_id,
        'profile_urn_id': profile.profile_urn_id,
        'profile_firstName': profile.profile_firstName,
        'profile_lastName': profile.profile_lastName,
        'profile_network_distance': profile.profile_network_distance,
        'profile_latest_company': profile.profile_latest_company,
        'profile_latest_job_title': profile.profile_latest_job_title,
        'category': profile.profile_category,
        'connection_req_withdrawn_status': False,
        'connection_req_withdrawn_date': None,
        'record_added_to_sheet': getCurrentDate()}

def get_concatinated_df(df1, df2):
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def remove_duplicates_from_df(df, unq_identifier_col):
    return df.drop_duplicates(subset=[unq_identifier_col])

def get_cols_to_update(original_list, sublist):
    new_list = [item for item in original_list if item not in sublist]
    return new_list

def get_common_rows(df1, df2):
    common_rows = df1.merge(df2, on='profile_urn_id', how='inner', suffixes=('', '_y'))
    common_rows = common_rows[df1.columns]
    return common_rows

def get_uncommon_rows(df1, df2):
    not_common_rows = df2[~df2['profile_urn_id'].isin(df1['profile_urn_id'])]
    return not_common_rows