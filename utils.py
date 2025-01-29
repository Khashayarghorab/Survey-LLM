import pandas as pd
import re
import os
import json
from io import StringIO
from google.oauth2 import service_account
import gspread
import streamlit as st

@st.cache_data
def extract_tables(markdown_text):
    """
    Extracts tables from Markdown text and returns them as a list of DataFrames.
    """
    tables = []
    pattern = re.compile(r'(\|.+?\|(?:\n\|[-:]+)+\n(?:\|.*?\|(?:\n|$))+)', re.DOTALL)
    matches = pattern.findall(markdown_text)
    for match in matches:
        table = pd.read_csv(StringIO(match), sep='|').dropna(axis=1, how='all').dropna(axis=0, how='all')
        tables.append(table)
    return tables

def display_response(response_text):
    """
    Displays the response text, rendering Markdown and tables appropriately.
    """
    tables = extract_tables(response_text)
    for table in tables:
        st.table(table)
        response_text = response_text.replace(table.to_markdown(), '')

    st.markdown(response_text)



def log_to_google_sheet(selection, model, question, task, name, email, gender, age, experience, role, ai_usage, familiarity_jsa, comments):
    try:
        """
        Logs the user's selection to Google Sheets.
        """
        # Check if running locally or on Streamlit Cloud
        if os.path.exists("credentials.json"):
            # Load credentials locally
            with open("credentials.json") as f:
                service_account_info = json.load(f)
        else:
            # Load credentials from Streamlit Cloud's st.secrets
            service_account_info = st.secrets["gcp_service_account"]

        # Authenticate with Google Sheets API
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        # Use gspread to access Google Sheets
        client = gspread.authorize(credentials)

        # Open your Google Sheet by name
        
        sheet = client.open_by_key("1Fn7mX6JsvKqJEammSZbtE_s_RJCmzQfjK8KBXQr2ZEM").sheet1

        # Add a new row with the data
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([current_time, task, selection, model, question, name, email, gender, age, experience, role, ai_usage, familiarity_jsa, comments])
    except Exception as e:
        st.error(f"Failed to log response to Google Sheets: {e}")
