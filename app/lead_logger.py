import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
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