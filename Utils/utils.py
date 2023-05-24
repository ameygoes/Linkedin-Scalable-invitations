from datetime import datetime
import json
import os

from Configs.envrinomentSpecificConfgis import CACHE_FILE
from Configs.jobConfigs import FIRSTNAME, LASTNAME, PUBLIC_PROFILE_ID


def getCurrentTime():
    return datetime.now()

def getTotalTime(totalSeconds):
    hours = int(totalSeconds // 3600)
    minutes = int((totalSeconds % 3600) // 60)
    seconds = int(totalSeconds % 60)
    return hours, minutes, seconds

def writeJSONfile(filepath, data):
    # Write the JSON object to a file.
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def readJSONfile(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def get_id_from_urn(urn):
    return urn.split(":")[3]


def cache_public_profile_id(api):
    """
    Caches the public profile id of the logged in user.
    """

    # Check if the file exists.
    if os.path.isfile(CACHE_FILE):

        # Get the size of the file.
        file_size = os.path.getsize(CACHE_FILE)

        # Check if the file is empty.
        if file_size == 0:
            # Write the profile to the file.
            writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

        # Read the profile from the file.
        cache_profile = readJSONfile(CACHE_FILE)

        # Check if the profile is up-to-date.
        if cache_profile["firstName"] == FIRSTNAME and cache_profile["lastName"] == LASTNAME:
            return cache_profile

        # The profile is not up-to-date, so write the new profile to the file.
        writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

        return readJSONfile(CACHE_FILE)

    # The file does not exist, so write the profile to the file.
    writeJSONfile(CACHE_FILE, api.get_profile(public_id=PUBLIC_PROFILE_ID))

    return readJSONfile(CACHE_FILE)

    