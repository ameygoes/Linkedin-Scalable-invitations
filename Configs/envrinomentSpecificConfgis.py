from Configs.dbConfigs import PRD_DB_NAME, PROFILE_TABLE, PROFILE_TABLE_TEST, TEST_DB_NAME
from Configs.runable_configs import ENVIRONMENT 
import os

from Utils.osUtils import getBaseDir

CRED_FOLDER_PATH = os.environ.get("CREDS_PATH")
SCHEDULING_CONFIGS = os.path.join(getBaseDir(), "Configs", "schedulers_configs.json")
if ENVIRONMENT.lower() == 'prod':
    CONFIGURATION_FILE = os.path.join(getBaseDir(), "Params","prod","jobParams.yaml")
    CACHE_FILE = os.path.join(getBaseDir(), "Cache","prod","personal_info.json")
    CREDS_FILE = os.path.join(CRED_FOLDER_PATH,"prod_key.key")
    DB_NAME = PRD_DB_NAME
    TABLE_NAME = PROFILE_TABLE
else:
    CONFIGURATION_FILE = os.path.join(getBaseDir(), "Params","test","jobParams.yaml")
    CACHE_FILE = os.path.join(getBaseDir(), "Cache","test","personal_info.json")
    CREDS_FILE = os.path.join(CRED_FOLDER_PATH,"dev_key.key")
    DB_NAME = TEST_DB_NAME
    TABLE_NAME = PROFILE_TABLE_TEST
