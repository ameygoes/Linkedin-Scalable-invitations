import urllib.parse
import requests
import os
import json
import pandas as pd
from Main.login import Login
from urllib.parse import quote
from linkedin_api.utils import helpers
# # Define the encoded URL
# encoded_url = 'https://www.linkedin.com/search/results/people/?company=qwe&connectionOf=%22ACoAACCgK-EBCubqo8WRfhf5fPxhmywyly11wLE%22&currentCompany=%5B%221441%22%2C%224787%22%5D&firstName=qwe&followerOf=%22ACoAAB72UEIBGWmnuwU_dQLmCThcwPlaI4lFJMk%22&geoUrn=%5B%22103644278%22%5D&keywords=recruiters&lastName=qwe&network=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH&pastCompany=%5B%221681%22%2C%221586%22%5D&schoolFilter=%5B%224292%22%2C%22166632%22%5D&sid=xEf&titleFreeText=qwe'
encoded_url = "https://www.linkedin.com/voyager/api/graphql?variables=(lazyLoadedActionsUrns:List(urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAAAMDh-EByAl6hN0wOj4Bzwt_WNQo353rCgg,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAAAi6mi4ByzqjkunjJn2rBPwrD4Ke8VcX7AE,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAAB-txa4BSCi8O_TWE7jnUhEyrruybtSqWJ0,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAAB0qrW4BoIxVHKq78xPL3prke2rjla95GcU,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAAByyP5IB4HQS6H9cbZX-Zd-C08JmDSGL5EI,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAACGCBUwB820RVl_y4dagR_neFilA3Wbvctw,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAADGHBnkBRtvpkLwXHi7bikHA_iTxBT4JtRs,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAADOIl04BMhFl3UUldfV6XpMJAZoVAcPw-ck,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAADP0RTsBPEOASDPp9x7DafLl3-VzX4y-Fv4,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP),urn:li:fsd_lazyLoadedActions:(urn:li:fsd_profileActions:(ACoAADQP1DoBC5jrlPYRvJ2qmGg5priWPVNkGTw,SEARCH_STATEFUL_COMPLIMENTARY,EMPTY_CONTEXT_ENTITY_URN),PEOPLE,SEARCH_SRP)))&&queryId=voyagerSearchDashLazyLoadedActions.9efa2f2f5bd10c3bbbbab9885c3c0a60"
# # Decode the URL
decoded_url = urllib.parse.unquote(encoded_url)

# # Parse the decoded URL
parsed_url = urllib.parse.urlparse(decoded_url)

# # Extract the base URL
base_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path

# Extract the parameters
params = urllib.parse.parse_qs(parsed_url.query)

# Print the base URL and parameters
print("Base URL:", base_url)
print("Parameters:", params)
api = Login()

def getCompanyID(company_link):
    try:
        company_username = company_link.split('.com/company/')[1].replace('/','')
    except:
        print("Wrong Company URL. Company Format should be https://www.linkedin.com/company/company_Username/!")
        return None
    
    api_link = 'https://www.linkedin.com/voyager/api/organization/companies?decorationId=com.linkedin.voyager.deco.organization.web.WebCompanyStockQuote-2&q=universalName&universalName={}'.format(quote(company_username))
    resp = api._get(api_link).json()
    company_id = resp.get('elements')[0].get('entityUrn').split(':')[-1]
    return company_id

"""
# import urllib.parse
# from bs4 import BeautifulSoup
# base_url = "https://www.linkedin.com/search/results/people"

# params = {
#     'company': 'google',
#     'connectionOf': '', # '"XYZ"' XYZ is public string it should be quoted like this
#     'currentCompany': '[]',
#     'firstName': '',
#     'followerOf': '', # '"XYZ"' XYZ is public string it should be quoted like this
#     'geoUrn': '["103644278"]', # This is code for USA
#     'keywords': 'recruiters',
#     'lastName': '',
#     'network': '["S","O"]',
#     'origin': 'GLOBAL_SEARCH_HEADER', #'FACETED_SEARCH',
#     'pastCompany': '[]',
#     'schoolFilter': '[]',
#     'sid': 'xEf',
#     'titleFreeText': ''
# }

# # Iterate over the dictionary and remove key-value pairs with value as None or empty list
# params = {key: value for key, value in params.items() if value is not None and value != '[]' and value !=''}
# params = {key: ','.join(value) if isinstance(value, list) else value for key, value in params.items()}
# print(params)

# # Convert the list values to string
# # params = {key: ','.join(value) if isinstance(value, list) else value for key, value in params.items()}

# # Encode and concatenate the parameters
# encoded_params = urllib.parse.urlencode(params)
# url = base_url + '?' + encoded_params
# response = api._get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Find the container or elements that contain the profile information
# profiles = soup.find_all('div', class_='entity-result')  # Adjust the class name as per the HTML structure
    
# print("Generated URL:", url)
# print(profiles)
"""
def fetch_employees(company_id, fetch_page_details, offset=0):

    
    variables = build_filters_query(
    keywords="Recruiters",
    currentCompany=[1441],
    network=["S", "O"],
    geoUrn=[103644278],
    title=[],
    resultType=["PEOPLE"],
    # Keywords inside filters
    company=[],
    firstName=[],
    lastName=None,
    connectionOf=["ACoAACA_posBXPv9QQFXGy_vfqpNAG98I_4awFE"],
    followerOf=[],
    # list of strings
    talksAbout=[],
    industry=[],
    pastCompany=[],
    profileLanguage=[],
    schoolFilter=[],
    schoolFreetext=[],
    searchId=["b418ee28-c4de-4324-a085-ffe3525acddd"],
    )
    uri = "/graphql?" + variables
    r = api._fetch(uri.format(offset=offset))

    if not r.ok:
        print(f"[fetch_employees()]: Fail! LinkedIn returned status code {r.status_code} ({r.reason})")
        return

    print(f"[fetch_employees()]: OK! LinkedIn returned status code {r.status_code} ({r.reason})")
    r = r.json()

    # print(json.dumps(r, indent=2))
    if not r["data"]["searchDashClustersByAll"]:
        print(f"Bad json. LinkedIn returned error:", r["errors"][0]["message"])
        return
    if fetch_page_details:
        return r["data"]["searchDashClustersByAll"]["paging"]["count"], r["data"]["searchDashClustersByAll"]["paging"]["total"]
    return r["data"]["searchDashClustersByAll"]

def write_to_scv(l):
    df = pd.DataFrame(l)
    df.to_csv("target.csv", mode='a', header=False, index=False)

def get_employees2(company_id, offset=0):
    def get_entity_attribute(entity, keys):
        if isinstance(keys, str):
            keys = [keys]

        current_entity = entity
        for key in keys:
            current_entity = current_entity.get(key)
            if not current_entity:
                return ""

        return current_entity

    records_per_page, total_num_records = fetch_employees(company_id, True)
    print(records_per_page, total_num_records)
    total_num_pages = total_num_records // records_per_page
    employees = []
    for page in range(3):
        print(f"page = {page}")
        employees_data = fetch_employees(company_id, False, offset=page*records_per_page)
        if not employees_data or employees_data.get("_type") != "com.linkedin.restli.common.CollectionResponse":
            # return []
            continue


        for cluster in employees_data.get("elements", []):
            if cluster.get("_type") != "com.linkedin.voyager.dash.search.SearchClusterViewModel":
                continue

            for item in cluster.get("items", []):
                if item.get("_type") != "com.linkedin.voyager.dash.search.SearchItem":
                    continue

                entity_result = item.get("item", {}).get("entityResult")
                if not entity_result or entity_result.get("_type") != "com.linkedin.voyager.dash.search.EntityResultViewModel":
                    continue
                print(entity_result)
                try:
                    employee = {
                        "title": get_entity_attribute(entity_result, ["title", "text"]),
                        "entityUrn": get_entity_attribute(entity_result, "entityUrn").split(":fsd_profile:")[1].split(",")[0],
                        "primarySubtitle": get_entity_attribute(entity_result, ["primarySubtitle", "text"]),
                        "secondarySubtitle": get_entity_attribute(entity_result, ["secondarySubtitle", "text"]),
                        "network": get_entity_attribute(entity_result, ["entityCustomTrackingInfo", "memberDistance"])
                    }
                    employees.append(employee)
                    # print(f"{employee} from {page}")
                except Exception as e:
                    print(f"Exception {e} occurred while processing employees of id {company_id}")
                    exit(1)

    return employees


def build_filters_query(keywords, offset_placeholder="{offset}", **kwargs):
    filters = []
    for key, value in kwargs.items():
        if value is not None and value != "" and value != []:
            if isinstance(value, list):
                value_list = ','.join(map(str, value))
                filters.append(f"(key:{key},value:List({value_list}))")
            else:
                filters.append(f"(key:{key},value:List({value}))")
    if filters:
        variables = f"variables=(start:{offset_placeholder},origin:FACETED_SEARCH,query:(keywords:{keywords},flagshipSearchIntent:SEARCH_SRP,queryParameters:List({','.join(filters)}),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.b0928897b71bd00a5a7291755dcd64f0"
        return variables
    else:
        return ""


# Print name of first 10 employees
company = api.get_company("google")
company_id = helpers.get_id_from_urn(company["entityUrn"])
getList = get_employees2(company_id)
write_to_scv(getList)
