import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("EMAIL_RECIPIENT")
        self.smtp_server = "smtp.gmail.com" # Default to Gmail
        self.smtp_port = 587

    def send_email(self, subject: str, body: str, image_path: str = None):
        """Send email with the article content."""
        if not self.sender_email or not self.password:
            print("Warning: Email credentials not set. Skipping email.")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            if image_path and os.path.exists(image_path):
                # Attach image logic here if needed
                pass

            print(f"--- Sending Email to {self.recipient_email} ---")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            print("Email Sent Successfully.")
            
        except Exception as e:
            print(f"Failed to send email: {e}")
