
import json
import os
import re
from app import BIND_TEST_CASE_FOLDER, TEST_SUITES_DIR


def get_testsuites(directory=TEST_SUITES_DIR, extension=".py"):
    """
    Recursively get all .py filenames inside the given directory without the .py extension.
    
    Args:
        directory (str): The base directory to search in.
        
    Returns:
        list: A list of Python filenames without .py extension (e.g., ['regression', 'list'])
    """
    python_files = set()  # Use a set to avoid duplicates
    
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                if file == "test_suite_runner.py":
                    continue
                filename_without_ext = os.path.splitext(file)[0]  # Remove .py extension
                python_files.add(filename_without_ext)
    return sorted(list(python_files))  # Sort for consistency

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
        
def format_feature(feature_string):
    # input: @feature, output: feature.feature
    # Remove special characters (like @, #, etc.)
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", feature_string)
    
    # Append `.feature` extension
    formatted_filename = f"{sanitized}.feature"
    
    return formatted_filename

def parse_feature_file(file_path):
    feature_data = {
        "feature": "",
        "scenarios": []
    }
    
    scenario = None
    examples = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            # Capture feature title
            if line.startswith("Feature:"):
                feature_data["feature"] = line.replace("Feature:", "").strip()

            # Capture Scenario or Scenario Outline
            elif line.startswith("Scenario:") or line.startswith("Scenario Outline:"):
                if scenario:
                    if examples:
                        scenario["examples"] = examples
                    feature_data["scenarios"].append(scenario)
                
                scenario_type = "Scenario Outline" if line.startswith("Scenario Outline:") else "Scenario"
                scenario = {
                    "type": scenario_type,
                    "scenario": line.replace("Scenario:", "").replace("Scenario Outline:", "").strip(),
                    "steps": [],
                    "examples": []
                }
                examples = []

            # Capture steps (Given, When, Then, And, But)
            elif re.match(r"^(Given|When|Then|And|But) ", line):
                if scenario:
                    scenario["steps"].append(line)
            
            # Capture Examples table
            elif line.startswith("Examples:"):
                examples = []

            elif "|" in line:  # Table row (Example data)
                if scenario:
                    examples.append(line.strip())

        # Append the last scenario
        if scenario:
            if examples:
                scenario["examples"] = examples
            feature_data["scenarios"].append(scenario)

    return feature_data