from Configs.runable_configs import ENVIRONMENT 
import os

if ENVIRONMENT.lower() == 'prod':
    CONFIGURATION_FILE = os.path.join("..", "Params" ,"jobParams.yaml")

else:
    CONFIGURATION_FILE = os.path.join("..", "Params" ,"jobParams.yaml")
