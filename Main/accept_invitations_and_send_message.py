from login import Login
from Configs.messageConfigs import accept_invite_message_body
from Configs.jobConfigs import *
from datetime import datetime 

"""
# def rejectInvitation(invitation, api, invitationEntityURN, sharedSecret, entity, action):
    # invitationEntityURN = invitation['entityUrn']
    # sharedSecret = invitation['sharedSecret']
    # response = api.reply_invitation(invitation_entity_urn = invitationEntityURN,
    # invitation_shared_secret = sharedSecret,
    # entity=entity,
    # action=action
    # )
    # return response
"""

# ACCEPT INVITATION
def acceptInvitation(invitation, api):
    # FETCH DATA
    # INVITATOIN SENDER DETAILS
    fromMember = invitation['fromMember']
    fromFirstName = fromMember['firstName']
    fromLastName = fromMember['lastName']

    # INVITATOIN RECEIVER DETAILS
    sharedSecret = invitation['sharedSecret']
    invitationEntityURN = invitation['entityUrn']
    
    print("================================================================")
    print(f"Processing invitation from user: {fromFirstName} {fromLastName} ... ⌛️")
    
    # ACCEPT OR REJECT INVITATION
    return api.reply_invitation(invitation_entity_urn = invitationEntityURN,
                                invitation_shared_secret = sharedSecret
                                )

# SENDS MESSAGE
def send_message(invitation, api):

    # PARSE DATA
    fromMember = invitation['fromMember']
    fromFirstName = fromMember['firstName']
    fromLastName = fromMember['lastName']
    fromUser = fromMember['dashEntityUrn']
    invitationSentToMember = invitation['toMember']['firstName']
    toMailBoxURN = invitation['toMember']['dashEntityUrn']

    print(f"Sending First Message to user: {fromFirstName} {fromLastName} 💬")
    return api.send_message(
            mailBoxURN = toMailBoxURN,
            message_body = accept_invite_message_body.format(
                toFirstName = fromFirstName,
                portFolioURL = PORTFOLIO,
                fromFirstName = invitationSentToMember
            ),
            recipients = [fromUser]
    )

      
def main():
    accept_invite_message_body
    api = Login()

    # GET INVITATIONS
    invitations_recevied = api.get_invitations(limit=LIMIT)

    
    if len(invitations_recevied) == 0:
        print("No invitations found!")
    
    # LOOP THROUGH INVITATIONS
    else:
        for invitation in invitations_recevied:
            
            # FOR HANDELING NEWS LETTER INVITATIONS
            if 'fromMember' not in invitation.keys():
                # For the Future version of the script, we need to check if there are any such invitations.
                # res = rejectInvitation()
                print("Skipping invitations for NewsLetter ❌")
                # Reject these requests.

            # FOR HANDELING INVITATIONS FROM PEOPLE
            else:
                response = acceptInvitation(invitation, api)
                    
                if response:

                    print("Invitation accepted ✅")
                    
                    # IF INVITATOIN IS ACCEPTED, SEND MESSAGE
                    res = send_message(invitation, api)
                    
                    if not res:
                        print("Message sent ✅")
                    else:
                        print("Message not sent ❌")
                # IF ERROR OCCURRED, CONTINUE
                else:
                    print("Error in accepting Invitation ❌")
# CALL FUNCTION
main()