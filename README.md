# Installation:
1. Install python
2. Install virtual environment: python -m venv env
3. Activate environment: .\env\Scripts\activate
4. Install all required libraries: pip install -r requirements.txt
5. Run Test suite

# Run test suite
python run.py <test_suite_name>

# Alternative way to run:
./test <test_suite_name>

# Run with allure:
behave -f allure_behave.formatter:AllureFormatter -o reports/json features/
allure serve reports/
