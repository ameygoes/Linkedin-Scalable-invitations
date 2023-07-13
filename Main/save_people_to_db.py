import pandas as pd
from Entity.profile import Profile
from Configs.dbConfigs import FETCH_COMPANY_PEOPLE, FETCH_COMPANY_PEOPLE_FOR_OFFSET, INSERT_QUERY_PROFILE, PROFILE_TABLE_COLUMNS
from Configs.envrinomentSpecificConfgis import TABLE_NAME
from Configs.jobConfigs import COMPANY_NAME, KEYWORD_TITLE, MAX_LINKEDIN_API_CALLS_LIMIT, NETWORK_DEPTHS, REGION, SEARCH_RESULT_LIMIT
from Main.login import Login
from Utils.dbUtils import insert_bulk_data, execute_get_command, readSQLQueryinPD
from Utils.utils import get_df_items_for_search_results, get_id_from_urn, get_overall_category, get_scheduler_config, get_uncommon_rows, remove_duplicates_from_df, update_schedulers_config
from linkedin_api.utils.helpers import generateUUID


# LOGIN TO LINKEDIN
api = Login()

# Assuming your DataFrame is named df
category_searching = get_overall_category(KEYWORD_TITLE)
    
# FETCH EXISTING DATA FROM GOOGLE SPREADSHEET
OFFSET_LIMIT = execute_get_command(FETCH_COMPANY_PEOPLE_FOR_OFFSET.format(TABLE_NAME, COMPANY_NAME.lower(), category_searching.lower()))[0][0]
print(f"Getting results from: {OFFSET_LIMIT} to {OFFSET_LIMIT + SEARCH_RESULT_LIMIT}")

# WE ARE ALLOWED TO MAKE AROUND 500 CALLS TO LINKEDIN PER HOURS TO PREVENT IT FROM MARKING AT AS A BOT
# WE WILL USE 350 AS PER HOUR LIMIT FOR SAFE SIDE
# TOTAL CALLS TO LIKNEDIN: LIMIT + 2 SO OUR LIMIT SHOULD NOT EXCEED 348 IN TOTAL
total_no_of_api_calls_to_lk = get_scheduler_config('total_number_of_api_calls_to_linkedin')

if (MAX_LINKEDIN_API_CALLS_LIMIT - total_no_of_api_calls_to_lk - SEARCH_RESULT_LIMIT) > 0:

    try:
        # CREATING AN EMPTY LIST TO STORE PEOPLE FROM SEARCH
        people_from_search_json_list = []

        print("Getting Company ID")
        company = api.get_company(COMPANY_NAME)
        company_id = get_id_from_urn(company["entityUrn"])
        

        # CALL TO SEARCH PEOPLE
        print(f"Searching for People on Linkedin, with search parameters: \
            KEYWORD_TITLE: {KEYWORD_TITLE} \n\
            LIMIT: {SEARCH_RESULT_LIMIT} \n\
            OFFSET: {OFFSET_LIMIT} \n\
            COMPANY: {COMPANY_NAME} \n\
            NETWORK_DEPTH: {NETWORK_DEPTHS}")
        results = api.search_peoplev2(
                            keywords=KEYWORD_TITLE,
                            limit=SEARCH_RESULT_LIMIT,
                            offset=OFFSET_LIMIT,
                            currentCompany=[company_id],
                            network=[NETWORK_DEPTHS],
                            geoUrn=[REGION],
                            title=[],
                            resultType=["PEOPLE"],
                            # Keywords inside filters
                            company=[],
                            firstName=[],
                            lastName=None,
                            connectionOf=[],
                            followerOf=[],
                            # list of strings
                            talksAbout=[],
                            industry=[],
                            pastCompany=[],
                            profileLanguage=[],
                            schoolFilter=[],
                            schoolFreetext=[],
                            searchId=[generateUUID()]                           
                            )

        # LOOPING OVER TO FETCH PEOPLE DATA FROM GET_PROFILE API AND PARSING RESULTS INTO OBJECT
        for peopleJSON in results:
            profile = Profile()
            
            # GET PROFILE
            peopleProfile = api.get_profile(peopleJSON["urn_id"])

            if peopleProfile:
                # PROFILE PARSING
                profile.parseProfileJSON(peopleProfile)
                profile.parseSearchPeopleJSON(peopleJSON)
            
                # APPENDING TO LIST
                people_from_search_json_list.append(get_df_items_for_search_results(profile))
            print(profile)
        # CONVERTING LIST TO A DATAFRAME
        df_people_from_search = pd.DataFrame(people_from_search_json_list, columns=PROFILE_TABLE_COLUMNS)
        df_people_from_db = readSQLQueryinPD(FETCH_COMPANY_PEOPLE.format(TABLE_NAME, COMPANY_NAME.lower(), category_searching))
        
        # # GET THE NEW ROWS TO BE ADDED TO GOOGLE SPREADSHEET
        new_rows_added_df = get_uncommon_rows(df_people_from_db, df_people_from_search)

        # # REMOVE DUPLICATES
        no_duplicates_df = remove_duplicates_from_df(new_rows_added_df, unq_identifier_col='profile_urn_id')

        # # UPDATE DATA IN THE DB
        insert_bulk_data(no_duplicates_df, INSERT_QUERY_PROFILE.format(TABLE_NAME))
        # gsheet.update_spreadsheet(no_duplicates_df)

        update_schedulers_config('total_number_of_api_calls_to_linkedin',  total_no_of_api_calls_to_lk + SEARCH_RESULT_LIMIT + 2)
        
    except Exception as e:
        print(f"Exception Occured:\n {e}")
        update_schedulers_config('total_number_of_api_calls_to_linkedin',  total_no_of_api_calls_to_lk)
else:
    print("Max api calls to linkedin exceeded. Try after an hour.")
