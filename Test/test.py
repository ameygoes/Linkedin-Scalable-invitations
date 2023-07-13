from Configs.jobConfigs import COMPANY_NAME, KEYWORD_TITLE
from Main.login import Login

from Utils.utils import get_id_from_urn, getProfileCategory

api = Login()

# jsonData = api.get_profile("ACoAJXf0dUsB4KwFP02mCyhS3q-serKwXPHHNDA-yU")
# print(json.dumps(jsonData, indent=2))
company = api.get_company(COMPANY_NAME)
company_id = get_id_from_urn(company["entityUrn"])
print(COMPANY_NAME, company_id)