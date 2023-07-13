from datetime import datetime
import json
import os
import pandas as pd
from Configs.envrinomentSpecificConfgis import CACHE_FILE, SCHEDULING_CONFIGS
from Configs.jobConfigs import FIRSTNAME, LASTNAME, PUBLIC_PROFILE_ID
from fuzzywuzzy import fuzz

# CATEGORIES FOR DECIDING
categories = [
    "hr",
    "data"
]
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
    if urn:
        return urn.split(":")[3]
    return urn
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

    if job_title:
        # Threshold for matching percentage (70% in this example)
        match_threshold = 80

        # Predefined job titles
        predefined_titles = ["Recruiter", "Technical Recruiter", "Talent Acquisition Specialist", "Senior Recruiter", "Corporate Recruiter", "Executive Recruiter", "IT Recruiter", "Campus Recruiter", "Staffing Specialist", "Sourcing Specialist"]

        # Check if the jobTitle partially matches any job title from the list
        matches = [title for title in predefined_titles if fuzz.partial_ratio(job_title.lower(), title.lower()) >= match_threshold]

        # If there are any matches, assign the category "HR"
        category = "hr" if matches else "data"
        
        return category
    return "default_category"

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
        'connection_req_sent_status': False,
        'connection_req_sent_date': None,
        'record_added_to_db': getCurrentDate()}

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

def update_schedulers_config(property_name, value):
    data = readJSONfile(SCHEDULING_CONFIGS)
    data[property_name] = value
    writeJSONfile(SCHEDULING_CONFIGS, data)

def get_scheduler_config(property_name):
    data = readJSONfile(SCHEDULING_CONFIGS)
    return data[property_name]

def get_overall_category(search_list):
    max_score = -1
    overall_category = None

    for category in categories:
        score = max(fuzz.partial_ratio(search_term.lower(), category.lower()) for search_term in search_list)
        if score > max_score:
            max_score = score
            overall_category = category

    return overall_category

def get_offset_count(counts, category):
    hr_count = counts.get('HR', 0)
    dev_count = counts.get('DATA', 0)

    if category == 'HR':
        return hr_count + 1
    return dev_count + 1
   