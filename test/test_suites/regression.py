# insert the tags to run in your test_suite
tags = [
        "@appointment", 
        "@login"
        ]

def run_suite():
    from subprocess import run
    from test import FEATURE_DIR

    # Build the tags argument for behave command
    tags_argument = f"--tags={','.join(tags)}"

    # Run behave with the tags for this suite
    run(["behave", FEATURE_DIR, tags_argument, "-f", "allure_behave.formatter:AllureFormatter", "-o", "reports/json"])

    # if you want to run with debugging
    # result = run(["behave", FEATURE_DIR, tags_argument], capture_output=True, text=True)
    # Print the output for debugging
    # print(result.stdout)
    # print(result.stderr)
