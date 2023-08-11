# first import all required Module
import io
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import re
class Drive_OCR:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        # self.credentials = "./credentials.json"
        # self.pickle = "./token.pickle"
        self.credentials = "google_ocr/credentials.json"
        self.pickle = "google_ocr/token.pickle"

    def main(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        # print('File ID: %s' % file.get('id'))

        # It will export drive image into Doc
        request = service.files().export_media(fileId=file.get('id'),mimeType="text/plain")

        # For Downloading Doc Image data by request
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))

        # It will delete file from drive base on ID
        service.files().delete(fileId=file.get('id')).execute() 

        # It will print data into terminal
        output = fh.getvalue().decode()
        # output = re.sub(r'[^\u0600-\u06FF\s]+', '', output)
        return output[17:]

# if __name__ == '__main__':
#     ob = Drive_OCR(r"D:\ticker_new\Dunya_Ticker\SFFODBV13SPTK8KF73KR.jpg")
#     '''
#     رکاو میں ڈامیں تو آہنی ہاتھوں میں کے ، اعلامیہ
#     '''
#     print(ob.main())


# pip install google_drive_ocr

# from google_drive_ocr import GoogleOCRApplication
# import os
# import re
# def Drive_OCR(image_path):
#     print('I am image',image_path)
#     app = GoogleOCRApplication("credentials.json")
#     result=app.perform_ocr(image_path)
#     print('result',result)
#     file_path = os.path.basename(image_path).replace("jpg","google.txt")
     
#     file_path=f'{os.path.splitext(image_path)[0]}.google.txt'
#     print('file_path',file_path)
#     with open(file_path, 'r', encoding='utf-8') as file:
#         text = file.read()
#     os.remove(file_path)
#     print('text',text)
#     text = re.sub(r'[^\u0600-\u06FF\s]+', '', text)


#     return text

