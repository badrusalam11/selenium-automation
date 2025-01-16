import os
from subprocess import run

def run_test_suite():
    print(os.getcwd())
    feature_dir = os.path.join(os.getcwd(), "app")
    run(["behave", feature_dir, "--tags=@login"])

