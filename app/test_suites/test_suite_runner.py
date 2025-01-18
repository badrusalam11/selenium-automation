import os
from subprocess import run
from app import FEATURE_DIR

def run_test_suite():
    # feature_dir = os.path.join(os.getcwd(), "app")
    run(["behave", FEATURE_DIR, "--tags=@appointment"])

