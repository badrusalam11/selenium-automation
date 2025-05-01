from test import CONFIG_DATA, PROPERTIES_DATA, REPORTS_PDF_FOLDER
from test.external.omnirunner import OmniRunner
from test.utils.report import Report
from test.utils.email import Email
from test.utils.session_manager import session_manager  # Import the session manager

class EventUtil:
    def __init__(self):
        self.report = Report()
        self.properties = PROPERTIES_DATA
        self.report_folder = REPORTS_PDF_FOLDER
        self.email = Email()
        self.config = CONFIG_DATA
        self.omnirunner = OmniRunner()
        
    def after_test_suite(self, all_scenarios):
        properties = self.properties
        self.report.generate_json_report(all_scenarios)
        report_path = None
        for report in properties['report_extension']:
            if report == 'PDF':
                report_path = self.report.generate_pdf_report()
                if properties['is_send_mail'].lower()=="true":
                    self.email.send_mail(properties['tester_email'], "Test report", "this is test report", report_path)
            
            if self.config['omnirunner']['enable'] and report == 'PDF':
                running_data = session_manager.load_running_id()
                id_test = running_data['running_id']
                if report_path:  # Add the report path to the status update
                    print("report_path", report_path)
                    self.omnirunner.update_status(id_test, "All step executed", 3, report_path)
                else:
                    print("report_path is None")
                    self.omnirunner.update_status(id_test, "All step executed", 3)

    def after_step(self, step_data):
        if self.config['omnirunner']['enable']:
            running_data = session_manager.load_running_id()
            id_test = running_data['running_id']
            print("id_test", id_test)
            self.omnirunner.update_status(id_test, step_data['name'], step_data['status'])