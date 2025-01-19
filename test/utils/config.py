import configparser
import os
from test import (
    PROPERTIES_FILE, 
    SESSIONS_FOLDER, 
    REPORTS_JSON_FOLDER, 
    REPORTS_PDF_FOLDER
)

class Config:
    def ensure_folders_exist():
        for folder in [SESSIONS_FOLDER, REPORTS_JSON_FOLDER, REPORTS_PDF_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def load_properties():
        # Create a ConfigParser object to read the properties file
        config = configparser.ConfigParser()

        # Read the properties file
        config.read(PROPERTIES_FILE)

        # Convert the config into a dictionary
        properties = {}
        for key, value in config.items("DEFAULT"):  # Read from the default section
            # Check if the value contains commas and parse it into a list
            if "," in value:
                properties[key] = value.split(",")
            else:
                properties[key] = value
        return properties