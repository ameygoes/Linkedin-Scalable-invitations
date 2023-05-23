from datetime import datetime
import yaml

def getCurrentTime():
    return datetime.now()

def getTotalTime(totalSeconds):
    hours = int(totalSeconds // 3600)
    minutes = int((totalSeconds % 3600) // 60)
    seconds = int(totalSeconds % 60)
    return hours, minutes, seconds


def readYML(filepath):
    # Load the YAML file
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return data

def readConfigurations(filepath):
    
    data = readYML(filepath)
    

    # Print the updated data
    return data
