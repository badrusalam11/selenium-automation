import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from test import CONFIG_DATA

class Email:
    def __init__(self):
        """
        Initialize the Email class with sender credentials and SMTP configuration.
        """
        self.sender_email = CONFIG_DATA['email']['username']
        self.sender_password = CONFIG_DATA['email']['password']
        self.smtp_server = CONFIG_DATA['email']['smtp_server']
        self.smtp_port = CONFIG_DATA['email']['smtp_port']

    def send_mail(self, recipient_email, subject, body, file_path):
        """
        Sends an email with a PDF attachment.
        :param recipient_email: Email address of the recipient.
        :param subject: Subject of the email.
        :param body: Body content of the email.
        :param file_path: Path to the PDF file to attach.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: The file at {file_path} does not exist.")
            return
        
        # Create the email
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach the email body
        message.attach(MIMEText(body, "plain"))

        # Attach the file
        try:
            with open(file_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}",
            )
            message.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

        # Send the email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Start TLS encryption
                server.login(self.sender_email, self.sender_password)
                sendmail = server.sendmail(self.sender_email, recipient_email, message.as_string())
                print(sendmail)            
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
