import os
import json
import gspread

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(
    os.getenv("GOOGLE_CREDENTIALS")
)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds,
    scope
)

client = gspread.authorize(creds)

sheet = client.open(
    "Royal_divine_lead"
).sheet1


def save_lead(
    session_id,
    name,
    email,
    phone,
    product,
    quantity,
    country,
    question
):

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session_id,
        name,
        email,
        phone,
        product,
        quantity,
        country,
        question
    ])