from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from simple_scheduler.event import event_scheduler as scheduler

from os.path import exists
from datetime import datetime as dt
from zipfile import ZipFile

#authorization
creds = None
if exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/drive.file"])
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("cred.json", ["https://www.googleapis.com/auth/drive.file"])
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
service = build('drive', 'v3', credentials=creds)

def proccess():
    #making archive
    with ZipFile('traccar.zip', 'w') as fl:
        fl.write('database.vm.db')
        fl.write('traccar.xml')

    #uploading file
    service.files().create(body={'name': f'traccar_{dt.now().strftime("%d.%m.%Y")}.zip'}, media_body=MediaFileUpload('traccar.zip',\
        mimetype='text/plain', resumable=True)).execute()
    print(f'uploaded file traccar_{dt.now().strftime("%d.%m.%Y")}')

    #removing old files
    response = service.files().list(orderBy='createdTime').execute()['files']
    while len(response) > 3:
        service.files().delete(fileId=response[0]['id']).execute()
        print(f'deleted file {response[0]["name"]}')
        response.remove(response[0])

scheduler.add_job(target=proccess, tz='US/Central', when=['*|04:00'])