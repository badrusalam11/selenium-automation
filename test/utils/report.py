from datetime import datetime
import os
from test import REPORTS_PDF_DIR, RESULTS_FILE, SCREENSHOTS_DIR
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

class Report:
    # Ensure report directory exists
    if not os.path.exists(REPORTS_PDF_DIR):
        os.makedirs(REPORTS_PDF_DIR)

    @staticmethod
    def generate_pdf_report(SESSION):
        print(SESSION)
        ss_running_session_dir_arr = []
        for session in SESSION:
            ss_running_session_dir = os.path.join(SCREENSHOTS_DIR, session)
            ss_running_session_dir_arr.append(ss_running_session_dir)
        print(ss_running_session_dir_arr)
        
        # PDF filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_filename = os.path.join(REPORTS_PDF_DIR, f"Test_Report_{timestamp}.pdf")

        # Create a canvas
        pdf = canvas.Canvas(pdf_filename, pagesize=letter)
        pdf.setTitle("Test Execution Report")
        width, height = letter

        # Add a title
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
                    test_results.append(line.strip().split(","))  # Assuming CSV format
        else:
            test_results = [["Test Case", "Status", "Execution Time", "Screenshot"]]

        # Add a table for test results
        pdf.drawString(50, height - 110, "Test Results:")
        table_data = [["Test Case", "Status", "Execution Time", "Screenshot"]] + test_results
        table = Table(table_data, colWidths=[150, 100, 120, 150])

        # Style the table
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Add table to PDF
        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 50, height - 300)

        # Add screenshots
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
