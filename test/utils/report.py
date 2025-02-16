import json
import os
from pathlib import Path
import time
from datetime import datetime
from test import PROPERTIES_DATA, RESULTS_FILE, SCREENSHOTS_DIR, SESSIONS_FOLDER, REPORTS_JSON_FOLDER, REPORTS_PDF_FOLDER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from test.utils.config import Config
from test.utils.formatter import Formatter

class Report:
    def get_report_name(self, folder_path, extension="json"):
        timestamp = Formatter.get_timestamp()
        report_name = os.path.join(folder_path, f"{timestamp}_Test_Report.{extension}")
        return report_name

    def generate_json_report(self, all_scenarios):
        print(all_scenarios)
        # report_path = os.path.join(REPORTS_JSON_FOLDER, f"{timestamp}_Test_Report.json")
        report_path= self.get_report_name(REPORTS_JSON_FOLDER, 'json')
        with open(report_path, "w") as report_file:
            json.dump(all_scenarios, report_file, indent=4)
        print(f"JSON Report generated: {report_path}")
        return report_path

    def generate_pdf_report(self):
        print("PROPERTIES_DATA", PROPERTIES_DATA)
        tester_name = PROPERTIES_DATA['tester_name']
        report_json_path = self.get_report_name(REPORTS_JSON_FOLDER, "json")
        report_pdf_path = self.get_report_name(REPORTS_PDF_FOLDER, "pdf")
        
        # Load the JSON data
        with open(report_json_path, "r") as file:
            report_data = json.load(file)
        
        # Set up the PDF document
        doc = SimpleDocTemplate(report_pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title = Paragraph("Test Report", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Tester name
        tester_name_section = Paragraph(f"Tester Name: {tester_name}", styles["Heading2"])
        elements.append(tester_name_section)
        elements.append(Spacer(1, 12))
        
        # Iterate over features
        for feature in report_data:
            feature_name = f"Feature: {feature['feature_name']}"
            feature_paragraph = Paragraph(feature_name, styles["Heading2"])
            elements.append(feature_paragraph)
            
            scenario_name = f"Scenario: {feature['scenario_name']} (Status: {feature['status']})"
            scenario_paragraph = Paragraph(scenario_name, styles["Heading3"])
            elements.append(scenario_paragraph)
            
            elements.append(Spacer(1, 6))
            
            # Create a table for steps
            step_data = [["Step Name", "Status", "Duration (ms)"]]
            for step in feature["steps"]:
                # Add step details
                step_data.append([
                    Paragraph(step["name"], styles["BodyText"]),
                    step["status"],
                    step["duration"]
                ])
                
                # Add screenshots in a separate row, ensuring no separation by vertical lines
                if step["images"]:
                    for image_path in step["images"]:
                        try:
                            img = Image(image_path)
                            # Dynamically resize the image with a larger maximum width
                            aspect_ratio = img.imageWidth / img.imageHeight
                            max_width = 300  # Increased width for readability
                            img_width = min(max_width, img.imageWidth)
                            img_height = img_width / aspect_ratio
                            img.drawWidth = img_width
                            img.drawHeight = img_height
                            
                            # Check if image is in the row and merge all columns
                            image_cells = [img, "", ""]  # Empty columns for merging
                            step_data.append(image_cells)
                        except Exception as e:
                            print(f"Failed to load image: {image_path}, Error: {e}")
                            image_cells = [Paragraph("Image not found", styles["BodyText"]), "", ""]
                            step_data.append(image_cells)

            # Add the table
            table = Table(step_data, colWidths=[200, 100, 100])
            
            # Dynamically apply the SPAN style for rows containing images
            row_styles = []
            for idx, row in enumerate(step_data):
                if isinstance(row[0], Image):  # Check if the first cell contains an image
                    row_styles.append(("SPAN", (0, idx), (2, idx)))  # Merge all columns for this row

            # Apply general table style
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ] + row_styles))  # Apply dynamic row styles

            elements.append(table)
            elements.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(elements)
        print(f"PDF report generated: {report_pdf_path}")
        return report_pdf_path


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
