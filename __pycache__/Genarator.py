from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import RGBColor
from docx2pdf import convert
import streamlit as st
from datetime import date
import pandas as pd
import subprocess
import os
from Email import SendEmail
from Utils import evaluateAngular


def replace_text_in_docx(input_docx_path, output_docx_path, replacements):
    doc = Document(input_docx_path)

    def apply_bold(run):
        run.font.bold = True

    for paragraph in doc.paragraphs:
        for old, new in replacements.items():
            if old in paragraph.text:
                for run in paragraph.runs:

                    if old in run.text:
                        run.text = run.text.replace(old, new)
                        apply_bold(run)  


    doc.save(output_docx_path)

def convert_docx_to_pdf(input_docx_path, output_pdf_path):
    convert(input_docx_path)



TEMPLATE_FILE = "TEMPLATE.docx"
OUTPUT_DIR = '.'

csv_file = st.sidebar.file_uploader('Upload your CSV Files here')

if csv_file and type(st.session_state.get('data')) != pd.DataFrame:
  st.session_state.data = pd.read_csv(csv_file)

elif not csv_file:
  st.info('Upload CSV File to use Interface...')

if type(st.session_state.get('data')) == pd.DataFrame:
  email_subject = st.text_input('Enter Email Subject here', placeholder='Angular Strings are Accepted')
  email_body = st.text_area('Enter Email Body here', placeholder='Angular Strings are Accepted')

  if email_body and email_subject:
      send_email = st.button('Send Email(s)')

      if send_email:
        for index, row in st.session_state.data.iterrows():
          row_name = row['Name'].upper()
          row_domain = row['Domain']
          row_email = row['Email']

          row_subject = evaluateAngular(index, email_subject)
          row_body = evaluateAngular(index, email_body)
          
          with st.spinner(f'Creating Letter for {row_name}'):
            replacements = {
            '<NAME>': row_name,
            '<DOMAIN>': row_domain,
            '<DATE>': str(date.today().strftime('%d/%m/%Y')),  
            '<PERIOD>': '3 Months'
            }
            
            output = f'DNYX Intern Offer Letter - {row_name}'
            replace_text_in_docx(TEMPLATE_FILE, output + '.docx', replacements)

            convert_docx_to_pdf(output + '.docx', OUTPUT_DIR)

            os.remove(output + '.docx')

          with st.spinner(f'Mailing Letter to {row_name} [**{row_email}**]'):
            try:
              email = SendEmail(row_email, row_subject, row_body, f'{output}.pdf')
              email.sendMessage()
            except:
              st.error(f'Cannot Send Mail to {row_name} [{row_email}]')

            os.remove(output + '.pdf')
          
        st.success('Sent Mails Successfully...')






