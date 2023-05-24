from Entity.urnPrefixes import Prefix
from Utils.utils import get_id_from_urn


class Profile:
    def __init__(self):
        self.public_id = None,
        self.profile_urn_id = None,
        self.profile_summery = None,
        self.profile_industry_name = None,
        self.profile_industry_urn = None,
        self.profile_firstName = None,
        self.profile_lastName = None,
        self.profile_location = None,
        self.profile_location_geo_urn_id = None,
        self.profile_latest_company = None,
        self.profile_latest_company_urn = None,
        self.profile_member_urn = None,
        self.profile_school_urn_id = None,
        self.profile_network_distance = None,
        self.invitation_shared_secret = None,
        self.invitation_entity_urn = None

    def __repr__(self):
        return f"Profile(FirstName: {self.profile_firstName} LastName: {self.profile_lastName})"
    
    def parseProfileJSON(self, profile_json):

    # GET PROFILE DETAILS
        self.profile_summery = profile_json['summary']
        self.public_id = profile_json['public_id']
        self.profile_urn_id = get_id_from_urn(profile_json['entityUrn'])

    
    # GET PERSONAL DETAILS
        self.profile_firstName = profile_json['firstName']
        self.profile_lastName = profile_json['lastName']

    # GET LOCATION AND COMPANY DETAILS
        self.profile_location = profile_json['geoCountryName']
        self.profile_location_geo_urn_id = profile_json['geoCountryUrn']

        if len(profile_json['experience']):
            self.profile_latest_company = profile_json['experience'][0]['companyName']
            self.profile_latest_company_urn = get_id_from_urn(profile_json['experience'][0]['companyUrn'])

    # GET ADDITIONAL DETAILS
        self.profile_member_urn = profile_json['memberUrn']
        self.profile_industry_name = profile_json['industryName']
        self.profile_industry_urn = profile_json['industryUrn']

        if len(profile_json['education']):
            self.profile_school_urn_id = get_id_from_urn(profile_json['education'][0]['school'][0]['objectUrn'])

    def parseInvitationJSON(self, invitation_json):
        prefixes = Prefix()

        # SENDER DETAILS
        self.profile_urn_id = prefixes.get_dashedProfileEntityUrn(get_id_from_urn(invitation_json['fromMember']['dashEntityUrn']))
        self.profile_firstName = invitation_json['fromMember']['firstName']
        self.profile_lastName = invitation_json['fromMember']['lastName']
        

        # INVITATION DETAILS
        self.invitation_shared_secret = invitation_json['sharedSecret']
        self.invitation_entity_urn = prefixes.get_dashedInvitationUrn(get_id_from_urn(invitation_json['entityUrn']))



    

        