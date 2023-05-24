class Prefix:
    def __init__(self):
        # CONSTANT PREFIX
        self.constant_prefix="urn:li:"
        
        # LOCATION PREFIX
        self.geoUrn = "fs_geo:"
        
        # INDUSTRY PREFIXES
        self.industryUrn = "fs_industry:"
        
        # PROFILE PREFIX
        self.profileEntityUrn = "fs_profile:"
        self.dashedProfileEntityUrn = "fsd_profile:"
        self.miniProfileUrn = "fs_miniProfile:"
        self.memberUrn = "member:"
        
        # COMPANY PREFIX
        self.companyUrn = "fs_miniCompany:"
        self.dashedCompanyUrn = "fsd_company:"
        
        # SCHOOL PREFIX
        self.schoolObjectUrn = "school:"
        self.schoolEntityUrn = "fs_miniSchool:"
        
        # INVITATION PREFIX
        self.invitationRelUrn = "fs_relInvitation:"
        self.invitationMailBoxItemUrn = "invitation:"
        self.dashedInvitationUrn = "fsd_invitation:"


    def get_geoUrn(self, id):
        return self.constant_prefix + self.geoUrn + id

    def get_industryUrn(self, id):
        return self.constant_prefix + self.industryUrn + id

    def get_profileEntityUrn(self, id):
        return self.constant_prefix + self.profileEntityUrn + id

    def fsd_profile(self, id):
        return self.constant_prefix + self.dashedProfileEntityUrn + id

    def get_miniProfileUrn(self, id):
        return self.constant_prefix + self.miniProfileUrn + id

    def get_memberUrn(self, id):
        return self.constant_prefix + self.memberUrn + id

# SCHOOL COMPANY GETTERS
    def get_companyUrn(self, id):
        return self.constant_prefix + self.companyUrn + id

    def get_schoolObjectUrn(self, id):
        return self.constant_prefix + self.schoolObjectUrn + id

    def get_schoolEntityUrn(self, id):
        return self.constant_prefix + self.schoolEntityUrn + id

# INVITATIONS GETTERS
    def get_invitationRelUrn(self, id):
        return self.constant_prefix + self.invitationRelUrn + id

    def get_invitationMailBoxItemUrn(self, id):
        return self.constant_prefix + self.invitationMailBoxItemUrn + id

    def get_dashedInvitationUrn(self, id):
        return self.constant_prefix + self.dashedInvitationUrn + id
