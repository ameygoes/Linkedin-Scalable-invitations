from Configs.envrinomentSpecificConfgis import CONFIGURATION_FILE
from Utils.utils import readConfigurations

# READS THE CONFIGURATION FILE
configs = readConfigurations(CONFIGURATION_FILE)

# CACHE CONFIGURATION
PUBLIC_PROFILE_ID = configs['public_identifier']
FIRSTNAME = configs['first_name']
LASTNAME = configs['last_name']


# INVITAION CONFIGURATION
LIMIT = configs['limit']
PORTFOLIO = configs['portfolio']