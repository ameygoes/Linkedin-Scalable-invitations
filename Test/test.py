
import os
import json
import datetime




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

invitations_recevied = api.get_invitations(limit=1)

for invitation in invitations_recevied:
        if 'fromMember' not in invitation.keys():
                # invitationEntityURN = invitation['entityUrn']
                # sharedSecret = invitation['sharedSecret']
                # response = api.reply_invitation(invitation_entity_urn = invitationEntityURN,
                # invitation_shared_secret = sharedSecret,
                # entity="newsLetter",
                # action='reject'
                # )
                # print(response)
                print("Skipping invitations for NewsLetter ❌")
                # Reject these requests.

        else:
                fromMember = invitation['fromMember']
                fromFirstName = fromMember['firstName']
                fromLastName = fromMember['lastName']
                fromPublicIdentifier = fromMember['publicIdentifier']
                fromUser = fromMember['dashEntityUrn']
                fromTrackingId = fromMember['trackingId']

                invitationType = invitation['invitationType']
                sentTime = datetime.datetime.fromtimestamp(int(invitation['sentTime'])/ 1000).strftime('%Y-%m-%d')
                sharedSecret = invitation['sharedSecret']
                invitationEntityURN = invitation['entityUrn']
                invitationSentToMember = invitation['toMember']['firstName']
                mailBoxURN = invitation['toMember']['dashEntityUrn']

                print("================================================================")
                print(f"Processing invitation from user: {fromFirstName} {fromLastName} ... ⌛️")
                
                # ACCEPT OR REJECT INVITATION
                response = api.reply_invitation(invitation_entity_urn = invitationEntityURN,
                                invitation_shared_secret = sharedSecret,
                                action='accept'
                                )
                if response:
                        print("Invitation accepted ✅")
                        print(f"Sending First Message to user: {fromFirstName} {fromLastName} 💬")
                        res = api.send_message(
                                mailBoxURN = mailBoxURN,
                                message_body = message_body.format(
                                firstName = fromFirstName,
                                portFolioURL = "https://ameyportfolio.netlify.app/",
                                toFirstName = invitationSentToMember),
                                recipients = [fromUser]
                        )

                        if not res:
                                print("Message sent ✅")
                        else:
                                print("Message not sent ❌")
                else:
                        print("Error in accepting Invitation ❌")
                
                # print(f"Viewing Profile for user: {fromFirstName} {fromLastName} 👀")
                
                # res = api.view_profile(
                #         target_profile_public_id = fromPublicIdentifier,
                #         target_profile_member_urn_id = fromTrackingId
                # )

                # if not res:
                #         print("Profile Viewed 👀 ")
                # else:
                #         print("Profile not Viewed ❌")
