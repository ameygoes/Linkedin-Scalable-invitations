from linkedin_api import Linkedin
import json

credentials = {
    "username": "",
    "password": ""
}

linkedin = Linkedin(credentials["username"], credentials["password"])

profile_id = "ACoAABQ11fIBQLGQbB1V1XPBZJsRwfK5r1U2Rzw"

results = linkedin.search_people(schools=["17769"],keyword_title=["Data Engineer"],regions=["103644278"])

print(json.dumps(results,indent=2))

# profile = linkedin.get_profile(profile_id)

# print(json.dumps(profile))

# connections = linkedin.get_profile_connections(profile["profile_id"])

# print(json.dumps(connections))

# connection_public_id = ""
# message_str = "Hi, I would like to connect."

# status = linkedin.add_connection(connection_public_id, message_str)

# print(status)