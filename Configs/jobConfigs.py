from Configs.envrinomentSpecificConfgis import CONFIGURATION_FILE
import yaml

def readYML(filepath):
    # Load the YAML file
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return data

def readConfigurations(filepath):   
    data = readYML(filepath)
    # Print the updated data
    return data

# READS THE CONFIGURATION FILE
configs = readConfigurations(CONFIGURATION_FILE)

# CACHE CONFIGURATION
PUBLIC_PROFILE_ID = configs['public_identifier']
FIRSTNAME = configs['first_name']
LASTNAME = configs['last_name']


# INVITAION CONFIGURATION
INVITATION_LIMIT = configs['invitation_limit']
PORTFOLIO = configs['portfolio']

# GSUTILITY CONFIGURATION
ENCRYPTED_EMAIL = configs['encrypted_email']