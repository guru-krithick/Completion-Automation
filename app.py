import streamlit as st
import pandas as pd
from Generator import generate_certificate
from Email import SendEmail
import os

# Template and output paths
TEMPLATE_FILE = "TEMPLATE.docx"
OUTPUT_DIR = '.'  # Save the files to the current directory

# Function to replace placeholders in email subject and body
def replace_placeholders(text, name, role):
    """Replaces placeholders like <NAME> and <ROLE> in the email subject and body"""
    return text.replace('<NAME>', name).replace('<ROLE>', role)

# CSV file upload
csv_file = st.sidebar.file_uploader('Upload your CSV file here', type=['csv'])

if csv_file:
    st.session_state['data'] = pd.read_csv(csv_file)

if 'data' in st.session_state:
    # Email subject and body for Domain (Technical)
    email_subject_domain = st.text_input('Enter Email Subject for Technical Domain here', 
        value='🎉 Congrats, <NAME>! You’ve Successfully Completed Your Internship in <ROLE>!')

    email_body_domain = st.text_area('Enter Email Body for Technical Domain here', 
        value="""Dear <NAME>, We are thrilled to announce that you have successfully completed your 3-month internship in <ROLE> with DNYX Business Solutions! 🎉 Throughout this internship, you have demonstrated exceptional skills, passion, and commitment to excellence. We truly appreciate your hard work and the valuable contributions you’ve made during this period. As a token of our appreciation, please find your official certificate of internship attached to this email. We hope this serves as a testament to your dedication and achievements, and we are confident you will continue to thrive in your future endeavors. Wishing you all the best for your bright future ahead! Warm regards,\nRudhresh S\nFounder & CEO\nDNYX Business Solutions
""")

    # Email subject and body for Field (Non-Technical)
    email_subject_field = st.text_input('Enter Email Subject for Non-Technical Field here', 
        value='🎉 Kudos, <NAME>! You’ve Successfully Completed Your Training in <ROLE>!')

    email_body_field = st.text_area('Enter Email Body for Non-Technical Field here', 
        value="""Dear <NAME>, Congratulations on successfully completing your training in <ROLE> with DNYX Business Solutions! Over the course of this program, you have shown remarkable dedication and a strong desire to learn, growing your expertise in this field. We’ve seen you develop critical skills that are essential in today's ever-evolving landscape, and we are certain these abilities will serve you well as you continue on your career path. Enclosed, you will find your official certificate of training, which we hope will be a testament to your commitment and achievements. Remember, every step you've taken during this training has prepared you to take on bigger challenges and seize new opportunities. We are excited to see where your journey takes you next, and we hope you’ll carry the knowledge and experience gained here into your future endeavors. Wishing you all the best for your bright future ahead! Warm regards,\nRudhresh S\nFounder & CEO\nDNYX Business Solutions
""")

    if email_subject_domain and email_body_domain and email_subject_field and email_body_field:
        send_email = st.button('Send Emails')

        if send_email:
            for index, row in st.session_state['data'].iterrows():
                row_name = row['Name'].strip()
                row_email = row['Email'].strip()
                row_domain = row['Domain'].strip() if pd.notna(row['Domain']) else None
                row_field = row['Field'].strip() if pd.notna(row['Field']) else None

                # Process Domain (Technical)
                if row_domain:
                    with st.spinner(f'Generating technical certificate for {row_name} - {row_domain}'):
                        pdf_path_domain = generate_certificate({'Name': row_name, 'Domain': row_domain}, TEMPLATE_FILE, OUTPUT_DIR)
                        st.success(f'Generated certificate for {row_domain}: {os.path.basename(pdf_path_domain)}')

                    # Replace placeholders in subject and body
                    customized_subject_domain = replace_placeholders(email_subject_domain, row_name, row_domain)
                    customized_body_domain = replace_placeholders(email_body_domain, row_name, row_domain)

                    with st.spinner(f'Sending technical email to {row_name} for {row_domain}'):
                        try:
                            email = SendEmail(row_email, customized_subject_domain, customized_body_domain, [pdf_path_domain])
                            email.sendMessage()
                            st.success(f'Email sent to {row_name} for {row_domain}')
                        except Exception as e:
                            st.error(f'Failed to send technical email to {row_name} for {row_domain}: {e}')

                    # Clean up generated PDF
                    try:
                        os.remove(pdf_path_domain)
                        st.success(f"Cleaned up generated PDF: {os.path.basename(pdf_path_domain)}")
                    except Exception as e:
                        st.error(f"Error cleaning up PDF for {row_name}: {e}")

                # Process Field (Non-Technical)
                if row_field:
                    with st.spinner(f'Generating non-technical certificate for {row_name} - {row_field}'):
                        pdf_path_field = generate_certificate({'Name': row_name, 'Domain': row_field}, TEMPLATE_FILE, OUTPUT_DIR)
                        st.success(f'Generated certificate for {row_field}: {os.path.basename(pdf_path_field)}')

                    # Replace placeholders in subject and body
                    customized_subject_field = replace_placeholders(email_subject_field, row_name, row_field)
                    customized_body_field = replace_placeholders(email_body_field, row_name, row_field)

                    with st.spinner(f'Sending non-technical email to {row_name} for {row_field}'):
                        try:
                            email = SendEmail(row_email, customized_subject_field, customized_body_field, [pdf_path_field])
                            email.sendMessage()
                            st.success(f'Email sent to {row_name} for {row_field}')
                        except Exception as e:
                            st.error(f'Failed to send non-technical email to {row_name} for {row_field}: {e}')

                    # Clean up generated PDF
                    try:
                        os.remove(pdf_path_field)
                        st.success(f"Cleaned up generated PDF: {os.path.basename(pdf_path_field)}")
                    except Exception as e:
                        st.error(f"Error cleaning up PDF for {row_name}: {e}") 