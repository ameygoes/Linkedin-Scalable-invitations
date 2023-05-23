from Configs.envrinomentSpecificConfgis import CONFIGURATION_FILE
from Utils.utils import readConfigurations

# READS THE CONFIGURATION FILE
configs = readConfigurations(CONFIGURATION_FILE)

LIMIT = configs['limit']
PORTFOLIO = configs['portfolio']