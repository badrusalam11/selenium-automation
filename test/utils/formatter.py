from datetime import datetime
import json
import os
from test import BIND_TEST_CASE_FOLDER


class Formatter:
    @staticmethod
    def str_to_bool(s: str) -> bool:
        """
        Convert a string to a boolean.

        Acceptable truthy values: 'true', '1', 'yes', 'y', 't'.
        Any other value will be considered False.

        Parameters:
            s (str): The input string.

        Returns:
            bool: True if the string is a truthy value, False otherwise.
        """
        return s.strip().lower() in ("true", "1", "yes", "y", "t")
    
    @staticmethod
    def get_timestamp() -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return timestamp
    
    def bind_test_case(test_case_file):
        test_case_path = os.path.join(BIND_TEST_CASE_FOLDER, test_case_file)
        if os.path.exists(test_case_path):
            print(f"Loading configuration from {test_case_path}...")
            try:
                with open(test_case_path, "r") as config_file:
                    config = json.load(config_file)
                    return config
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON file: {e}")
        else:
            raise FileNotFoundError("No bind test case found.")