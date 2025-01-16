import os
from subprocess import run

def run_test_suite():
    feature_dir = os.path.join(os.getcwd(), "features")
    run(["behave", feature_dir, "--tags=@login"])

if __name__ == "__main__":
    run_test_suite()
