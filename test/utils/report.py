import json
import os
from pathlib import Path
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from test import RESULTS_FILE, SCREENSHOTS_DIR, SESSIONS_FOLDER, REPORTS_JSON_FOLDER, REPORTS_PDF_FOLDER


class Report:
    @staticmethod
    def ensure_folders_exist():
        for folder in [SESSIONS_FOLDER, REPORTS_JSON_FOLDER, REPORTS_PDF_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    @staticmethod
    def generate_json_report(all_scenarios):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = os.path.join(REPORTS_JSON_FOLDER, f"{timestamp}_Test_Report.json")
        with open(report_path, "w") as report_file:
            json.dump(all_scenarios, report_file, indent=4)
        print(f"JSON Report generated: {report_path}")

    @staticmethod
    def generate_pdf_report(SESSION):
        print("Generating PDF Report...")

        ss_running_session_dir_arr = [
            os.path.join(SCREENSHOTS_DIR, session) for session in SESSION
        ]
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_filename = os.path.join(REPORTS_PDF_FOLDER, f"{timestamp}_Test_Report.pdf")
        pdf = canvas.Canvas(pdf_filename, pagesize=letter)
        pdf.setTitle("Test Execution Report")
        width, height = letter

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, height - 50, "Test Execution Report")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Read test results
        test_results = []
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, "r") as file:
                lines = file.readlines()
                for line in lines:
                    test_results.append(line.strip().split(","))
        else:
            test_results = [["Test Case", "Status", "Execution Time", "Screenshot"]]

        # Add a table for test results
        pdf.drawString(50, height - 110, "Test Results:")
        table_data = [["Test Case", "Status", "Execution Time", "Screenshot"]] + test_results
        table = Table(table_data, colWidths=[150, 100, 120, 150])

        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 50, height - 300)

        # Add screenshots for failed test cases
        pdf.drawString(50, height - 320, "Screenshots for Failed Test Cases:")
        y_position = height - 350
        for ss_running_session_dir in ss_running_session_dir_arr:
            if os.path.isdir(ss_running_session_dir):
                for screenshot in os.listdir(ss_running_session_dir):
                    screenshot_path = os.path.join(ss_running_session_dir, screenshot)
                    if os.path.isfile(screenshot_path):
                        pdf.drawString(50, y_position, f"Screenshot: {screenshot}")
                        pdf.drawImage(screenshot_path, 50, y_position - 100, width=200, height=100)
                        y_position -= 150
                        if y_position < 100:  # Start a new page if needed
                            pdf.showPage()
                            y_position = height - 50

        # Save the PDF
        pdf.save()
        print(f"PDF report generated: {pdf_filename}")

    @staticmethod
    def save_scenario_data(session_id, scenario_data):
        session_file = f"test/sessions/{session_id}.json"
        with open(session_file, "w") as file:
            json.dump(scenario_data, file, indent=4)

    @staticmethod
    def collect_all_scenarios_excluding_current():
        all_scenarios = []
        sessions_path = Path("test/sessions")
        for session_file in sessions_path.glob("*.json"):
            if session_file.name == "current_session.json":
                continue
            with open(session_file, "r") as file:
                scenario_data = json.load(file)
                all_scenarios.append(scenario_data)
        return all_scenarios

    @staticmethod
    def construct_step_data(step, start_time, images):
        """Construct step data with the given step details and timing."""
        end_time = int(time.time() * 1000)
        duration = end_time - start_time

        return {
            "name": step.name,
            "status": step.status.name,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "images":images
        }

    @staticmethod
    def create_scenario_data(context, scenario):
        """Creates a structured scenario report with all the steps and their details."""
        end_time = int(time.time() * 1000)
        execution_time = end_time - context.start_time

        scenario_data = {
            "feature_name": context.feature_name,
            "scenario_name": context.scenario_name,
            "status": "passed" if scenario.status.name == "passed" else "failed",
            "steps": context.steps,
            "duration": execution_time,
            "start_time": context.start_time,
            "end_time": end_time,
            "session_id": context.session_id,
        }

        return scenario_data
