from Configs.runable_configs import ENVIRONMENT 

if ENVIRONMENT.lower() == 'prod':
    CONFIGURATION_FILE = "../Params/jobParams.yml"

else:
    CONFIGURATION_FILE = "../Params/jobParams.yml"

