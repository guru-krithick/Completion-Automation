import streamlit as st

# Utility function to check if text contains Angular placeholders
def containsAngular(text):
    return (start := text.find('<')) and (end := text.find('>')) and abs(start - end) > 0

# Function to replace Angular strings with corresponding data from the CSV
def evaluateAngular(index, text):
    evaluation_dict = {
        '<NAME>' : 'Name',
        '<YEAR>' : 'Year',
        '<DOMAIN>' : 'Domain',
        '<TIME>' : 'Time'
    }

    if containsAngular(text):
        row = st.session_state.data.iloc[index]

        for template, constant_column in evaluation_dict.items():
            if text.find(template) > -1:
                text = text.replace(template, str(row[constant_column]))

    return text
