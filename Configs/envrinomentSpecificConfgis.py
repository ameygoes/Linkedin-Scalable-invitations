from Configs.runable_configs import ENVIRONMENT 
import os

if ENVIRONMENT.lower() == 'prod':
    CONFIGURATION_FILE = os.path.join("..", "Params","prod","jobParams.yaml")
    CACHE_FILE = os.path.join("..", "Cache","prod","personal_info.json")
else:
    CONFIGURATION_FILE = os.path.join("..", "Params","test","jobParams.yaml")
    CACHE_FILE = os.path.join("..", "Cache","test","personal_info.json")
