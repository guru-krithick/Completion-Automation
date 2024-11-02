import os
import smtplib
from email.message import EmailMessage
import streamlit as st

# Emailer class to handle email sending
class Emailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # Function to send an email with optional attachments
    def send(self, recipient, subject, body, attachments=None):
        msg = EmailMessage()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach multiple files if provided
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(f.name)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Send email using Gmail's SMTP server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(self.email, self.password)
        smtp_server.send_message(msg)
        smtp_server.quit()

# SendEmail class to facilitate email customization and sending
class SendEmail:
    def __init__(self, email, subject, body, attachments=None):
        # Here we use Streamlit secrets to retrieve credentials securely
        self.emailer = Emailer(st.secrets['EMAIL'], st.secrets['PASS_KEY'])
        self.receiver = email
        self.subject = subject
        self.body = body
        self.attachments = attachments

    # Method to send the email
    def sendMessage(self):
        self.emailer.send(self.receiver, self.subject, self.body, self.attachments) 