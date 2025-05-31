from speak_engine import speak, listen
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64, os, pickle

# Google API configurations
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'
CLIENT_SECRET_FILE = r"path_client_secret.json"
SENDER = "Email_sender"

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8888)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_email(to, subject, message_text):
    message = MIMEMultipart()
    message['From'] = SENDER
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(service, to, subject, message):
    msg = create_email(to, subject, message)
    service.users().messages().send(userId='me', body=msg).execute()

def voice_email():
    speak("Please enter the recipient's email address:")
    recipient = input("Recipient email: ")  # Take email as text input for better reliability

    # Ensure non-empty subject
    subject = None
    while not subject:
        speak("What is the subject?")
        subject = listen()
        if not subject:
            speak("I didn't catch that. Please say the subject again.")

    # Ensure non-empty message
    message = None
    while not message:
        speak("What should the message say?")
        message = listen()
        if not message:
            speak("I didn't catch that. Please say the message again.")

    speak(f"Sending email to {recipient}")

    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        send_email(service, recipient, subject, message)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")
        print(f"Error details: {e}")

# Function to be called from main.py
def send_mail():
    """Function to handle email sending commands"""
    voice_email()
