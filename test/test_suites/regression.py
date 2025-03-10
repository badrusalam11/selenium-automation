# insert the tags to run in your test_suite
from test.utils.formatter import Formatter
tags = Formatter.bind_test_case('regression.json')

def run_suite():
    from subprocess import run
    from test import TEST_DIR

    # Build the tags argument for behave command
    tags_argument = f"--tags={','.join(tags)}"

    # Run behave with the tags for this suite
    run(["behave", TEST_DIR, tags_argument])

    # if you want to run with debugging
    # result = run(["behave", TEST_DIR, tags_argument], capture_output=True, text=True)
    # Print the output for debugging
    # print(result.stdout)
    # print(result.stderr)
