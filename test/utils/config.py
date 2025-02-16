import configparser
import json
import os
from dotenv import load_dotenv
from test import (
    PROPERTIES_FILE, 
    SESSIONS_FOLDER, 
    REPORTS_JSON_FOLDER, 
    REPORTS_PDF_FOLDER
)
from test.utils.formatter import Formatter

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
    
    def load_config(config_path="config.json"):
        """
        Loads configuration data from an .env file if it exists.
        Otherwise, loads configuration from the provided JSON file.
        :param config_path: Path to the config.json file (used if .env is not found).
        :return: Dictionary containing the loaded configuration data.
        """
        config = {}
        # Check for .env file
        if os.path.exists(".env"):
            print("Loading configuration from .env file...")
            load_dotenv()  # Load environment variables from .env
            config['environment'] = os.getenv("ENVIRONMENT")
            config["email"] = {
                "username": os.getenv("EMAIL_USERNAME"),
                "password": os.getenv("EMAIL_PASSWORD"),
                "smtp_server": os.getenv("EMAIL_SMTP_SERVER"),
                "smtp_port": os.getenv("EMAIL_SMTP_PORT"),
                "enable_tls": Formatter.str_to_bool(os.getenv("EMAIL_ENABLE_TLS")),
            }
            return config

        # Fall back to config.json if .env not found
        if os.path.exists(config_path):
            print(f"Loading configuration from {config_path}...")
            try:
                with open(config_path, "r") as config_file:
                    config = json.load(config_file)
                    return config
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON file: {e}")
        else:
            raise FileNotFoundError("No configuration file found (.env or config.json).")
