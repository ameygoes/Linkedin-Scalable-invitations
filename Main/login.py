from linkedin_api import Linkedin
import os

linkedin_email = os.environ.get("LINKED_IN_UN_2") # place your linkedin login email
linkedin_password = os.environ.get("LINKED_IN_PASS_2") # place your linkedin login password

def Login():
    # Authenticate using any Linkedin account credentials
    return Linkedin(linkedin_email, linkedin_password)