from Configs.dbConfigs import FETCH_COMPANY_RECRUITERS_FOR_OFFSET
from Configs.envrinomentSpecificConfgis import TABLE_NAME
from Configs.jobConfigs import COMPANY_NAME, KEYWORD_TITLE
from Main.login import Login
from Utils.dbUtils import execute_get_command
from Utils.utils import get_overall_category

# LOGIN TO LINKEDIN
api = Login()

# Assuming your DataFrame is named df
category_searching = get_overall_category(KEYWORD_TITLE)

# FETCH EXISTING DATA FROM GOOGLE SPREADSHEET
OFFSET_LIMIT = execute_get_command(FETCH_COMPANY_RECRUITERS_FOR_OFFSET.format(TABLE_NAME, COMPANY_NAME.lower(), category_searching.lower()))[0][0]


# CALL TO SEARCH PEOPLE
results = api.search_people(
                            keyword_title=KEYWORD_TITLE,
                            regions=REGION,
                            network_depths=NETWORK_DEPTHS,
                            keyword_company=COMPANY_NAME,
                            limit=SEARCH_RESULT_LIMIT,
                            offset=OFFSET_LIMIT
                            )
# WE ARE ALLOWED TO MAKE AROUND 500 CALLS TO LINKEDIN PER HOURS TO PREVENT IT FROM MARKING AT AS A BOT
# WE WILL USE 350 AS PER HOUR LIMIT FOR SAFE SIDE
# TOTAL CALLS TO LIKNEDIN: LIMIT + 2 SO OUR LIMIT SHOULD NOT EXCEED 348 IN TOTAL
total_no_of_api_calls_to_lk = get_scheduler_config('total_number_of_api_calls_to_linkedin')

if (MAX_LINKEDIN_API_CALLS_LIMIT - total_no_of_api_calls_to_lk - SEARCH_RESULT_LIMIT) > 0:

    # CREATING AN EMPTY LIST TO STORE PEOPLE FROM SEARCH
    people_from_search_json_list = []

    # LOOPING OVER TO FETCH PEOPLE DATA FROM GET_PROFILE API AND PARSING RESULTS INTO OBJECT
    for peopleJSON in results:
        profile = Profile()
        
        # GET PROFILE
        peopleProfile = api.get_profile(peopleJSON["urn_id"])
        
        # PROFILE PARSING
        profile.parseProfileJSON(peopleProfile)
        profile.parseSearchPeopleJSON(peopleJSON)
        
        # APPENDING TO LIST
        people_from_search_json_list.append(get_df_items_for_search_results(profile))

    update_schedulers_config('total_number_of_api_calls_to_linkedin',  total_no_of_api_calls_to_lk + SEARCH_RESULT_LIMIT + 2)

    # CONVERTING LIST TO A DATAFRAME
    df_people_from_search = pd.DataFrame(people_from_search_json_list, columns=PROFILE_TABLE_COLUMNS)

    # GET THE NEW ROWS TO BE ADDED TO GOOGLE SPREADSHEET
    new_rows_added_df = get_uncommon_rows(df_people_from_db, df_people_from_search)
    concatinated_df = get_concatinated_df(df_people_from_db, new_rows_added_df)

    # REMOVE DUPLICATES
    no_duplicates_df = remove_duplicates_from_df(concatinated_df, unq_identifier_col='profile_urn_id')

    # UPDATE DATA IN GOOGLE SPREADSHEET
    gsheet.update_spreadsheet(no_duplicates_df)
else:
    print("Max api calls to linkedin exceeded. Try after an hour.")
