Run test suite
python features/test_suites/test_suite_runner.py

Run with allure:
behave -f allure_behave.formatter:AllureFormatter -o reports/json features/
allure serve reports/
