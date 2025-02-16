from test import PROPERTIES_DATA, REPORTS_PDF_FOLDER
from test.utils.report import Report
from test.utils.email import Email

class EventUtil:
    def __init__(self):
        self.report = Report()
        self.properties = PROPERTIES_DATA
        self.report_folder = REPORTS_PDF_FOLDER
        self.email = Email()

    def after_test_suite(self, all_scenarios):
        properties = self.properties
        self.report.generate_json_report(all_scenarios)
        for report in properties['report_extension']:
            if report == 'PDF':
                report_path = self.report.generate_pdf_report()
                if properties['is_send_mail'].lower()=="true":
                    self.email.send_mail(properties['tester_email'], "Test report", "this is test report", report_path)