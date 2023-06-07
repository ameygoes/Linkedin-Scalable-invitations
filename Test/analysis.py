# CALL TO SEARCH PEOPLE
from Configs.jobConfigs import *
from Main.login import Login
import json

api = Login()

# results = api.search_people(
#                             keyword_title=KEYWORD_TITLE,
#                             regions=REGION,
#                             network_depths=NETWORK_DEPTHS,
#                             keyword_company=COMPANY_NAME,
#                             limit=SEARCH_RESULT_LIMIT,
#                             offset=1
#                             )/

# results = api.get_profile("ACoAADzH7OYBxSSJAuFiHm1e_-dzTcBaXKYgVO4")
# print(results)

# Define the API URL
url = '/messaging/dash/presenceStatuses'

# Define the variables
variables = "/graphql?variables=(start:0,origin:FACETED_SEARCH,query:(keywords:recruiters,flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:geoUrn,value:List(103644278)),(key:network,value:List(S,O)),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.b0928897b71bd00a5a7291755dcd64f0"

# Define the query ID
query_id = 'voyagerSearchDashFilterClusters.762ab3bcd12981f5ebd753a9a2c36ff0'

# Create the request payload
payload = {"filters":["resultType->PEOPLE"],"keywords":"recruiters","origin":"FACETED_SEARCH","searchId":"03215588-abc5-43cf-b1fd-580ff73b412c"}
url = "/graphql?includeWebMetadata==true&variables=(start:0,origin:FACETED_SEARCH,query:(keywords:recruiters,flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:geoUrn,value:List(103644278)),(key:network,value:List(S,O)),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.b0928897b71bd00a5a7291755dcd64f0"
# Send the POST request to the API
response = api._fetch(url)
print(json.dumps(response.json(), indent=2))
# Get the response content
# data = response.json()

# # Handle the response as needed
# print(data)