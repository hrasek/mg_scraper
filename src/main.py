import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from dotenv import load_dotenv
from cukr_free_mg import mg_scraper

load_dotenv()

SENDER = os.getenv("email_from")
TO = os.getenv("email_to")
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gmail_authenticate():
    """Authenticate the user with OAuth 2.0 and return the Gmail API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def create_message(subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message["to"] = TO  # type: ignore
    message["from"] = SENDER  # type: ignore
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}


def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except Exception as error:
        print(f"An error occurred: {error}")


def main(message_text):
    # Authenticate and construct service.
    service = gmail_authenticate()

    # Specify email details
    sender = "hosekmotor1993@gmail.com"
    to = "hosekmotor1993@gmail.com"
    subject = "Test Email from Python"
    # message_text = "Hello, this is a test email sent from Python!"

    # Create email
    email_message = create_message(subject, message_text)

    # Send email
    send_message(service, "me", email_message)


if __name__ == "__main__":
    # print(mg_scraper.scrape_prices())

    main(str(mg_scraper.scrape_prices()))
