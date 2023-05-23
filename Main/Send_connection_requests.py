from login import Login
from Configs.messageConfigs import send_invite_to_receruiters_message_body, send_invite_to_developers_for_referral_message_body
from Configs.jobConfigs import *
from datetime import datetime 
      
def main():
    send_invite_to_receruiters_message_body
    send_invite_to_developers_for_referral_message_body

    api = Login()

    # GET Profiles to send invites to
    # Utils from DB or from GSheets or scrape new, return list of profiles
    profiles = []
    
    if len(profiles) == 0:
        print("No profiles found!")
    
    # LOOP THROUGH Profiles
    else:
        for profile in profiles:

            # Populate fields from config or parse from profile
            sendToName = ""
            myName = ""
            industryType = ""
            industryExp = ""
            companyName = ""
            skillsDescriptor = ""
            positionInterest = ""


            message_body_recruiter = send_invite_to_receruiters_message_body.format(
                        toFirstName = sendToName,
                        fromFirstName = myName,
                        fromIndustry = industryType,
                        fromExpInYears = industryExp,
                        toCompany = companyName
                    )
            message_body_developer = send_invite_to_developers_for_referral_message_body.format(
                        toFirstName = sendToName,
                        fromFirstName = myName,
                        max_4_skills = skillsDescriptor,
                        interested_position = positionInterest,
                        toCompany = companyName
                    )
            
            # FOR sending to recruiters
            if profile['category'] == "HR":
                api.add_connection(profile["publicId"],message_body_recruiter,profile["URN"])

            # FOR sending to developers
            elif profile['category'] == "DEV":
                api.add_connection(profile["publicId"],message_body_developer,profile["URN"])

# CALL FUNCTION
main()