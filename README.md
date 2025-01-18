Run test suite
python run.py <test_suite_name>

Alternative way to run:
./test <test_suite_name>

Run with allure:
behave -f allure_behave.formatter:AllureFormatter -o reports/json features/
allure serve reports/
