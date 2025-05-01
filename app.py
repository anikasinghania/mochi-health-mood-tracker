import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime
import numpy as np

# Credentials taken from secrets
creds_dict = st.secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Enabling sheet processing
spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
spreadsheet = client.open_by_url(spreadsheet_url)
sheet = spreadsheet.sheet1


# Streamlit UI with submittable actions
st.title('Mood Tracker')
mood = st.selectbox(
    "How are you feeling right now?",
    ["Happy", "Sad", "Stressed", "Overwhelmed", "Curious", "Annoyed", "Chill"]
)
note = st.text_area("Add a note (optional)", placeholder="What made you feel this way?")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# On submit 
if st.button('Submit'):
    # Appends the mood data and logs recently submitted info
    sheet.append_row([mood, note, timestamp])
    st.success(f"Mood logged: {mood}")
    if note:
        st.info(f"Note: {note}")
    else:
        st.info("No note provided.")


# Create a bar chart  
rows = sheet.get_all_values()
df = pd.DataFrame(rows[1:], columns=rows[0])
mood_options = df['Mood'].unique()
selected_moods = st.multiselect("Filter by Mood", options=mood_options, default=mood_options)
filtered_df = df[df['Mood'].isin(selected_moods)]
mood_counts = filtered_df['Mood'].value_counts()
st.bar_chart(mood_counts)

