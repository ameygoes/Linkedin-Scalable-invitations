from linkedin_api import Linkedin
import json

credentials = {
    "username": "",
    "password": ""
}

linkedin = Linkedin(credentials["username"], credentials["password"])

profile_id = "ACoAABQ11fIBQLGQbB1V1XPBZJsRwfK5r1U2Rzw"

profile = linkedin.get_profile(profile_id)

print(json.dumps(profile))

connections = linkedin.get_profile_connections(profile["profile_id"])

print(json.dumps(connections))

connection_public_id = ""
message_str = "Hi, I would like to connect."

status = linkedin.add_connection(connection_public_id, message_str)

print(status)