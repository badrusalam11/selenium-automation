import configparser
from app import PROPERTIES_FILE

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