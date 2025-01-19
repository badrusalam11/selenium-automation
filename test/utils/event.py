from test import PROPERTIES_DATA
from test.utils.report import Report

class EventUtil:
    def after_test_suite(all_scenarios):
        properties = PROPERTIES_DATA
        Report.generate_json_report(all_scenarios)
        for report in properties['report_extension']:
            if report == 'PDF':
                Report.generate_pdf_report()
