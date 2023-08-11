import io
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import multiprocessing
import os

class Drive_OCR:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials = "google_ocr/client_secret.json"
        self.pickle = "google_ocr/token.pickle"
        #self.credentials = "google_ocr/credentials.json"
        #self.pickle = "google_ocr/token.pickle"

    def main(self) -> str:
        starttime=time.time()
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
                # Set up Chrome options
                server_started = threading.Condition()
                # firefox_options = FirefoxOptions()
                # firefox_options.add_argument("--headless")  # Run Firefox in headless mode
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--incognito")
                #chrome_options.add_argument("--headless")
                print("options done")

                # Set path to GeckoDriver
                # webdriver_service = Service('drivers')  # Replace with driver path
                # print("driver found")

                # Create a new Firefox WebDriver instance
                # driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)
                driver = webdriver.Chrome(options=chrome_options)
                print("webdriver initialized")
                
                # Perform authentication flow using Selenium
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials, self.SCOPES)
                print("flow initialized")
                
                # Function to run the flow in the background
                def run_flow():
                    nonlocal creds
                    with server_started:
                        server_started.notify()
                    creds = flow.run_local_server(open_browser=False,port=2000)
                    

                # Start the flow in a separate thread
                flow_thread = threading.Thread(target=run_flow)
                flow_thread.start()
                with server_started:
                    server_started.wait(1)
                    print("server started")
                auth_url, _ = flow.authorization_url(prompt='consent')
                print("authorization url: ", auth_url)
                driver.get(auth_url)

                # Wait for the email input field to be available
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.ID, 'identifierId')))
                print("id found")

                # Enter email address
                email_input = driver.find_element(By.ID,'identifierId')
                email_input.click()
                email_input.send_keys('tickerocr@gmail.com')
                next_button = driver.find_element(By.ID, 'identifierNext')
                next_button.click()
                print("email done")

                # Wait for the password input field to be available
                wait.until(EC.presence_of_element_located((By.ID,'password')))
                print("name found")

                # Enter password
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type=password]')))
                password_input = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
                print("password field located")
                #password_input.click()
                password_input.send_keys('ticker@123')  # Replace with your password
                #password_input.submit()
                next_button = driver.find_element(By.ID, 'passwordNext')
                next_button.click()
                print("password done")

                # Back to safety screen
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button')))
                print("continue button clickable")
                continue_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button')
                print("continue button found")
                continue_button.click()
                
                # ocr wants access screen
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/button')))
                print("allow button clickable")
                continue_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/button')
                print("allow button found")
                continue_button.click()
                
                # Close the browser
                time.sleep(5)
                driver.quit()
                print("Authentication flow complete")

                # Wait for the flow to finish
                flow_thread.join()
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
           
       
        # os.remove(os.path.join('google_ocr','token.pickle'))

        endtime=time.time()
        print(f'OCRING DONE IN {endtime-starttime}seconds')
        # output = re.sub(r'[^\u0600-\u06FF\s]+', '', output)
        return output[17:]
        # result=output[17:]
        # output_queue.put(result)    # Put the result in the queue

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

