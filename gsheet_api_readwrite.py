from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import os

# Google Sheet details
#You can get the google sheet ID from the url of your google sheet.  It looks something like this:1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw
#Provide this as SHEET_ID in the function call.

# To allow the API to access your google sheet, share it with this email: 
# hackathon1@hackathon-452517.iam.gserviceaccount.com

# Path to save service account JSON key file
SERVICE_ACCOUNT_FILE = "serviceAccountCredsNew.json"

# Authenticate and build service
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                              scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=creds)


def googleSheetRead(RANGE="Sheet1!A2:A10", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Read a cell / range
    request = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE)
    response = request.execute()
    data = response.get("values", [])
    for row in data:
        print(row)  # Each row is a list of values
    return (data)


def googleSheetWrite(CELL="Sheet1!A2", VALUE="hello world", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Update a cell
    request = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=CELL,
        valueInputOption="RAW",
        body={"values": [[VALUE]]}
    )
    response = request.execute()
    print("Updated Cell:", response)
    return (response)


def googleSheetClear(RANGE="Sheet1!A1:B10", SHEET_ID = "get_sheet_ID_from_web_URL"):
    # Clear a range
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=RANGE,
        body={}
    ).execute()


if __name__ == "__main__":
    SHEET_ID = "1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw"

    data = googleSheetWrite(CELL="Sheet1!A3", VALUE="I am cell A3", SHEET_ID=SHEET_ID)
    more_data = googleSheetWrite(CELL="Sheet1!A5", VALUE="Test, testing, testing!", SHEET_ID=SHEET_ID)
    response = googleSheetRead(RANGE="Sheet1!A1:A10", SHEET_ID=SHEET_ID)


