import streamlit as st
import smtplib
from email.message import EmailMessage

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

        if attachment:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', int(st.secrets['PORT']))
        smtp_server.login(self.email, self.password)
        smtp_server.send_message(msg)
        smtp_server.quit()


class SendEmail:

    def __init__(self, email, subject, body, attachment=None):
        self.emailer = Emailer(st.secrets['EMAIL'], st.secrets['PASS_KEY'])
        self.receiver = email
        self.subject = subject
        self.body = body

        if attachment:
            self.attachment = attachment
        else:
            self.attachment = None

    def sendMessage(self):
        self.emailer.send(self.receiver, self.subject, self.body, self.attachment)
