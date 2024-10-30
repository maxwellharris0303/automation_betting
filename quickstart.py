from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1TLVUmV445G-GHz6N8FrozwzbiSfBqvn4AMKy_vGTTlk'
SAMPLE_RANGE_NAME = 'Sheet1!A2:I'


emailList = []

passwordList = []

columnCount = 0

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        emailList.clear()
        passwordList.clear()
        # print('Property Address, City:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if len(row) >= 2:
                emailList.append('%s' % (row[0]))
                passwordList.append('%s' % (row[1]))
        
        # print(getColumnCount())
        # print(getEmailList())
        # print(getPasswordList())
        # with open('data.txt', 'r', encoding='utf-8') as txt_file:
        #     txt_content = txt_file.readlines()

        # values = [[line.strip()] for line in txt_content if line.strip()]

        # insertContactInfo(f'Sheet1!A2', values)
    except HttpError as err:
        print(err)

def getEmailList():
    return emailList

def save_to_sheet():
    with open('data.txt', 'r', encoding='utf-8') as txt_file:
        txt_content = txt_file.readlines()

    values = [line.strip().split("\t") for line in txt_content if line.strip()]
    print(values)

    insertContactInfo(f'Sheet1!A2', values)


def getColumnCount():
    columnCount = len(emailList)
    return columnCount


def insertContactInfo(range_name, data):

    request_body = {
        'values': data
    }


    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Finally, call the API to write the data to the spreadsheet
        result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=request_body
            ).execute()

        print('{0} contact info updated.'.format(result.get('updatedCells')))
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()