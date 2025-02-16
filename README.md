# Installation
1. Install Python
2. Set up a virtual environment: `python -m venv env`
3. Activate the environment: `.\env\Scripts\activate`
4. Install required libraries: `pip install -r requirements.txt`
5. Run the test suite

# Run Test Suite
Run with: `python run.py <test_suite_name>`

# Alternative Run Command:
Use: `./test <test_suite_name>`

# Run with Allure
1. Run the tests with Allure: `behave test/features/ -f allure_behave.formatter:AllureFormatter -o reports/json`
2. Serve the report: `allure serve reports/`

# Configuration
To change the report extension output, update the `REPORT_EXTENSION` in `test.properties`:
- For both JSON and PDF: `REPORT_EXTENSION=JSON,PDF`
- For JSON only: `REPORT_EXTENSION=JSON`

# Docker build
docker build -t selenium-test .     