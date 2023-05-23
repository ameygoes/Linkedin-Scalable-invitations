from linkedin_api import Linkedin
import os
import json
import datetime


linkedin_email = os.environ.get("LINKED_IN_UN_2") # place your linkedin login email
linkedin_password = os.environ.get("LINKED_IN_PASS_2") # place your linkedin login password

# Authenticate using any Linkedin account credentials
api = Linkedin(linkedin_email, linkedin_password)

message_body = """
Hello {firstName},

Thank you for connecting with me on LinkedIn.
It would be very great to discuss any opprtunities with you on Data Engineering and Science.

I have my experties in Data, Automation and Cloud.
My PortFolio is available at {portFolioURL}

Lets keep in touch.
Thanks,
{toFirstName}
"""
# GET INVITATIONS ACCEPTS FOLLOWING PARAMETERS:
"""Fetch connection invitations for the currently logged in user.

:param start: How much to offset results by
:type start: int
:param limit: Maximum amount of invitations to return
:type limit: int

:return: List of invitation objects
:rtype: list
"""

invitations_recevied = api.get_invitations(limit=15)
# print(json.dumps(invitations_recevied))


for invitation in invitations_recevied:
        fromMember = invitation['fromMember']
        fromFirstName = fromMember['firstName']
        fromLastName = fromMember['lastName']
        fromPublicIdentifier = fromMember['publicIdentifier']
        invitationFromUser = fromMember['entityUrn']
        fromTrackingId = fromMember['trackingId']

        invitationType = invitation['invitationType']
        sentTime = datetime.datetime.fromtimestamp(int(invitation['sentTime'])/ 1000).strftime('%Y-%m-%d')
        sharedSecret = invitation['sharedSecret']
        invitationEntityURN = invitation['entityUrn']
        invitationSentToMember = invitation['toMember']['firstName']
        print("================================================================")
        print(invitationEntityURN, sharedSecret)
        print(f"Processing invitation from user: {fromFirstName} {fromLastName} ... ⌛️")
        
        response = api.reply_invitation(invitation_entity_urn = invitationFromUser,
                             invitation_shared_secret = sharedSecret
                             )
        print(response)
        if response:
                print("Invitation accepted ✅")
                print(f"Sending First Message to user: {fromFirstName} {fromLastName} 💬")
                res = api.send_message(
                        message_body.format(
                            firstName = fromFirstName,
                            portFolioURL = "https://ameyportfolio.netlify.app/",
                            toFirstName = invitationSentToMember),
                        recipients = [invitationFromUser]
                )

                if not res:
                        print("Message sent ✅")
                else:
                        print("Message not sent ❌")
        else:
                print("Error in accepting Invitation ❌")
        
        print(f"Viewing Profile for user: {fromFirstName} {fromLastName} 👀")
        
        res = api.view_profile(
                target_profile_public_id = fromPublicIdentifier,
                target_profile_member_urn_id = fromTrackingId
        )

        if not res:
                print("Profile Viewed 👀 ")
        else:
                print("Profile not Viewed ❌")
