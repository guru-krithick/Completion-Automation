import smtplib
from email.message import EmailMessage
import os
import streamlit as st

class Emailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, recipient, subject, body, attachment=None):
        msg = EmailMessage()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach file if provided
        if attachment:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                # Extract just the file name without the path
                file_name = os.path.basename(f.name)
            # Attach the file with the correct filename
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Send email using Gmail's SMTP server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(self.email, self.password)
        smtp_server.send_message(msg)
        smtp_server.quit()

class SendEmail:
    def __init__(self, email, subject, body, attachment=None):
        self.emailer = Emailer(st.secrets['EMAIL'], st.secrets['PASS_KEY'])
        self.receiver = email
        self.subject = subject
        self.body = body
        self.attachment = attachment

    def sendMessage(self):
        self.emailer.send(self.receiver, self.subject, self.body, self.attachment)
