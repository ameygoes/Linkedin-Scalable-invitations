from Configs.dbConfigs import PROD_TABLE_NAME, TEST_TABLE_NAME
from Configs.runable_configs import ENVIRONMENT 
import os

from Utils.osUtils import getBaseDir

CRED_FOLDER_PATH = os.environ.get("CREDS_PATH")
SCHEDULING_CONFIGS = os.path.join(getBaseDir(), "Configs", "schedulers_configs.json")
if ENVIRONMENT.lower() == 'prod':
    CONFIGURATION_FILE = os.path.join(getBaseDir(), "Params","prod","jobParams.yaml")
    CACHE_FILE = os.path.join(getBaseDir(), "Cache","prod","personal_info.json")
    CREDS_FILE = os.path.join(CRED_FOLDER_PATH,"prod_key.key")
    TABLE_NAME = PROD_TABLE_NAME
else:
    CONFIGURATION_FILE = os.path.join(getBaseDir(), "Params","test","jobParams.yaml")
    CACHE_FILE = os.path.join(getBaseDir(), "Cache","test","personal_info.json")
    CREDS_FILE = os.path.join(CRED_FOLDER_PATH,"dev_key.key")
    TABLE_NAME = TEST_TABLE_NAME
