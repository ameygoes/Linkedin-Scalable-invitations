from Entity.profile import Profile
from Utils.utils import cache_public_profile_id
from login import Login
from Configs.messageConfigs import accept_invite_message_body
from Configs.jobConfigs import *
from Entity.urnPrefixes import Prefix

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
    invitationProfile = Profile()
    invitationProfile.parseInvitationJSON(invitation)
    
    print("================================================================")
    print(f"Processing invitation from user: {invitationProfile.profile_firstName} {invitationProfile.profile_lastName} ... ⌛️")
    
    prefix = Prefix()
    # ACCEPT OR REJECT INVITATION
    return api.reply_invitation(invitation_entity_urn = prefix.get_dashedInvitationUrn(invitationProfile.invitation_entity_urn),
                                invitation_shared_secret = invitationProfile.invitation_shared_secret
                                )

# SENDS MESSAGE
def send_message(invitation, api):

    # PARSE INVITATION DATA
    invitation_sent_by_Profile = Profile()
    invitation_sent_by_Profile.parseInvitationJSON(invitation)
    
    # PARSE CACHE DATA
    invitation_sent_to_profile = Profile()
    cachedProfile = cache_public_profile_id(api)
    invitation_sent_to_profile.parseProfileJSON(cachedProfile)
    
    prefix = Prefix()
    print(f"Sending First Message to user: {invitation_sent_by_Profile.profile_firstName} {invitation_sent_by_Profile.profile_lastName} 💬")
    return api.send_message(
            mailBoxURN = prefix.fsd_profile(invitation_sent_to_profile.profile_urn_id),
            message_body = accept_invite_message_body.format(
                toFirstName = invitation_sent_by_Profile.profile_firstName,
                portFolioURL = PORTFOLIO,
                fromFirstName = invitation_sent_to_profile.profile_firstName
            ),
            recipients = [prefix.fsd_profile(invitation_sent_by_Profile.profile_urn_id)]
    )

      
def main():
    accept_invite_message_body
    api = Login()

    # GET INVITATIONS
    invitations_recevied = api.get_invitations(limit=INVITATION_LIMIT)

    
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