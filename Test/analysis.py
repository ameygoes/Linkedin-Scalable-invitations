from Configs.dbConfigs import PROFILE_TABLE_COLUMNS
from Entity.profile import Profile
from Main.login import Login
import pandas as pd
from Utils.gsutils import GoogleSheet

from Utils.utils import get_concatinated_df, get_df_items_for_search_results, get_uncommon_rows, remove_duplicates_from_df

api = Login()
df = pd.DataFrame(columns=PROFILE_TABLE_COLUMNS)
profile_id = "ACoAABQ11fIBQLGQbB1V1XPBZJsRwfK5r1U2Rzw"

results = api.search_people(
                            keyword_title=["Recruiter"],
                            regions=["103644278"],
                            network_depths=["S", "O"],
                            keyword_company="Google",
                            limit=20,
                            )

dataFrameData = []
for peopleJSON in results:
    profile = Profile()
    
    peopleProfile = api.get_profile(peopleJSON["urn_id"])
    profile.parseProfileJSON(peopleProfile)
    profile.parseSearchPeopleJSON(peopleJSON)
    dataFrameData.append(get_df_items_for_search_results(profile))


df_people_from_search = pd.DataFrame(dataFrameData, columns=PROFILE_TABLE_COLUMNS)


gsheet = GoogleSheet()
client = gsheet.authenticate()
df_people_from_gsheet = gsheet.get_spreadsheet_data(client)

new_rows_added_df = get_uncommon_rows(df_people_from_search, df_people_from_gsheet)
concatinated_df = get_concatinated_df(df_people_from_gsheet, new_rows_added_df)
no_duplicates_df = remove_duplicates_from_df(concatinated_df, unq_identifier_col='profile_urn_id')
pd.set_option('display.max_columns', None)
print(no_duplicates_df)
gsheet.update_spreadsheet(client, no_duplicates_df)
