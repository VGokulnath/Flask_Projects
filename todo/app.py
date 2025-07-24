from flask import Flask,render_template,request
import re
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import pytz
import json
import os
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds_dict = json.loads(os.getenv('GOOGLE_CREDS'))
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '10sBuEZLkLHQQhJ5qoNlG2_qzGnPvOzzXcX5ly13RGPc'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
sheet_service = build('sheets', 'v4', credentials=creds)

def extract_fields(text):
    text = re.sub(r'\r', '', text)  # Normalize line endings

    patterns = {
        'Date': r'Date:\s*(.*)',
        'Reviewer': r'Reviewer:\s*@?(.*)',
        'Extension Name': r'Extension Name:\s*(.*)',
        'Extension ID': r'Extension ID:\s*(.*)',
        'Revision': r'Revision:\s*(.*)',
        'Final Verdict': r'Final Verdict:\s*(.*)',
    }

    fields = {}
    ist = pytz.timezone('Asia/Kolkata')
    fields['Timestamp'] = datetime.now(ist).strftime('%B %d, %Y, %I:%M %p')
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Remove empty lines and strip trailing spaces
            value = match.group(1).strip()
            fields[key] = '\n'.join([line.strip() for line in value.splitlines() if line.strip()])
        else:
            fields[key] = 'Not Found'
    #fields['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return fields

def save_to_sheet(fields):
    values = [list(fields.values())]  # Convert dict to a single row
    body = {'values': values}

    sheet_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1',  # You can use 'A1' or 'Sheet1!A1' if your tab is named 'Sheet1'
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()



@app.route('/', methods=["GET", "POST"])
def index():
    extracted = None
    if request.method == "POST":
        input_text = request.form["doc_text"]
        extracted = extract_fields(input_text)

        df = pd.DataFrame([extracted])
        df.to_excel("output.xlsx", index=False)

        save_to_sheet(extracted) 
    return render_template("index.html", extracted=extracted)
