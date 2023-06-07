from Utils.utils import checkIfKeyExists, get_id_from_urn, getProfileCategory


class Profile:
    def __init__(self):
        # profile details
        self.public_id = None,
        self.profile_urn_id = None,
        self.profile_summery = None,
        self.profile_firstName = None,
        self.profile_lastName = None,
        self.profile_headline = None,

        # industry details
        self.profile_industry_name = None,
        self.profile_industry_urn = None,
        self.profile_school_urn_id = None,

        # company details
        self.profile_latest_company = "Your Company",
        self.profile_latest_company_urn = None,
        self.profile_latest_job_title = None,
        self.profile_category = None,

        # profile location
        self.profile_location = None,
        self.profile_location_geo_urn_id = None,
        
        # additional details
        self.profile_member_urn = None,
        self.profile_network_distance = None,
        self.invitation_shared_secret = None,
        self.invitation_entity_urn = None
        
    # def __repr__(self):
        # return (
        #     f"{self.__class__.__name__}("
        #     f"public_id={self.public_id}, \n "
        #     f"profile_urn_id={self.profile_urn_id},  \n"
        #     f"profile_summery={self.profile_summery},  \n"
        #     f"profile_firstName={self.profile_firstName},  \n"
        #     f"profile_lastName={self.profile_lastName}, \n "
        #     f"profile_headline={self.profile_headline},  \n"
        #     f"profile_industry_name={self.profile_industry_name},  \n"
        #     f"profile_industry_urn={self.profile_industry_urn},  \n"
        #     f"profile_school_urn_id={self.profile_school_urn_id},  \n"
        #     f"profile_latest_company={self.profile_latest_company},  \n"
        #     f"profile_latest_company_urn={self.profile_latest_company_urn},  \n"
        #     f"profile_latest_job_title={self.profile_latest_job_title},  \n"
        #     f"profile_category={self.profile_category},  \n"
        #     f"profile_location={self.profile_location},  \n"
        #     f"profile_location_geo_urn_id={self.profile_location_geo_urn_id}, \n "
        #     f"profile_member_urn={self.profile_member_urn},  \n"
        #     f"profile_network_distance={self.profile_network_distance}, \n "
        #     f"invitation_shared_secret={self.invitation_shared_secret},  \n"
        #     f"invitation_entity_urn={self.invitation_entity_urn}"
        #     ")"
        # )
    def __repr__(self):
        return f"Profile(FirstName: {self.profile_firstName} LastName: {self.profile_lastName} Category: {self.profile_category})"
    
    def parseProfileJSON(self, profile_json):
    
        # GET PROFILE DETAILS
        self.profile_summery = profile_json.get('summary')
        self.public_id = profile_json.get('public_id')
        self.profile_urn_id = get_id_from_urn(profile_json.get('entityUrn'))
        self.profile_headline = profile_json.get('headline')

        # GET PERSONAL DETAILS
        self.profile_firstName = profile_json.get('firstName')
        self.profile_lastName = profile_json.get('lastName')


        # GET LOCATION AND COMPANY DETAILS
        self.profile_location = profile_json.get('geoCountryName')
        self.profile_location_geo_urn_id = profile_json.get('geoCountryUrn')


        if profile_json.get('experience'):
            experience = profile_json['experience'][0]
            self.profile_latest_company = experience.get('companyName')
            self.profile_latest_job_title = experience.get('title')
            self.profile_category = getProfileCategory(self.profile_latest_job_title)
            if self.profile_latest_company != "Self-employed":
                self.profile_latest_company_urn = get_id_from_urn(experience.get('companyUrn'))


        # GET ADDITIONAL DETAILS
        self.profile_member_urn = profile_json.get('member_urn')
        self.profile_industry_name = profile_json.get('industryName')
        self.profile_industry_urn = profile_json.get('industryUrn')

        if profile_json.get('education'):
            education = profile_json['education'][0]
            if education.get('school'):
                self.profile_school_urn_id = get_id_from_urn(education['school'].get('objectUrn'))


    def parseInvitationJSON(self, invitation_json):

        # SENDER DETAILS
        self.profile_urn_id = get_id_from_urn(invitation_json['fromMember']['dashEntityUrn'])
        self.profile_firstName = invitation_json['fromMember']['firstName']
        self.profile_lastName = invitation_json['fromMember']['lastName']
        

        # INVITATION DETAILS
        self.invitation_shared_secret = invitation_json['sharedSecret']
        self.invitation_entity_urn = get_id_from_urn(invitation_json['entityUrn'])

    def parseSearchPeopleJSON(self, search_people_json):
        self.profile_network_distance = search_people_json["distance"]

    

        