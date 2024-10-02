import streamlit as st
import pandas as pd
from Generator import generate_certificate
from Email import SendEmail
import os
from datetime import date

# Template and output paths
TEMPLATE_FILE = "TEMPLATE.docx"
OUTPUT_DIR = '.'  # Save the files to the current directory

# Function to replace placeholders in email subject and body
def replace_placeholders(text, name, domain):
    return text.replace('<NAME>', name).replace('<DOMAIN>', domain)

# CSV file upload
csv_file = st.sidebar.file_uploader('Upload your CSV file here', type=['csv'])

if csv_file:
    st.session_state['data'] = pd.read_csv(csv_file)

if 'data' in st.session_state:
    email_subject = st.text_input('Enter Email Subject here', 
        value='🎉 Congrats, <NAME>! You’ve Successfully Completed Your Internship in <DOMAIN>!')

    email_body = st.text_area('Enter Email Body here', 
        value="""Dear <NAME>,\n
We are thrilled to announce that you have successfully completed your 3-month internship in <DOMAIN> with DNYX Business Solutions! 🎉\n
Throughout this internship, you have demonstrated exceptional skills, passion, and commitment to excellence. We truly appreciate your hard work and the valuable contributions you’ve made during this period.\n
As a token of our appreciation, please find your official certificate of internship attached to this email. We hope this serves as a testament to your dedication and achievements, and we are confident you will continue to thrive in your future endeavors.\n
Wishing you all the best for your bright future ahead!\n
Warm regards,\n
Rudhresh\n
Founder & CEO\n
DNYX Business Solutions
""")

    if email_subject and email_body:
        send_email = st.button('Send Emails')

        if send_email:
            for index, row in st.session_state['data'].iterrows():
                row_name = row['Name'].strip()  # Strip extra spaces around the name
                row_domain = row['Domain']
                row_email = row['Email']

                # Generate the certificate for the row
                with st.spinner(f'Generating certificate for {row_name}'):
                    pdf_path = generate_certificate(row, TEMPLATE_FILE, OUTPUT_DIR)

                    # Ensure we only use the file name for attachment
                    st.success(f'Generated certificate: {os.path.basename(pdf_path)}')

                # Replace placeholders in the email subject and body
                customized_subject = replace_placeholders(email_subject, row_name, row_domain)
                customized_body = replace_placeholders(email_body, row_name, row_domain)

                # Send the certificate via email
                with st.spinner(f'Sending email to {row_name}'):
                    try:
                        email = SendEmail(row_email, customized_subject, customized_body, pdf_path)
                        email.sendMessage()
                        st.success(f'Email sent to {row_name}')
                    except Exception as e:
                        st.error(f'Failed to send email to {row_name}: {e}')

                # Clean up the generated PDF after sending
                try:
                    os.remove(pdf_path)
                    st.success(f"Cleaned up generated PDF for {row_name}")
                except Exception as e:
                    st.error(f"Error cleaning up PDF for {row_name}: {e}")
