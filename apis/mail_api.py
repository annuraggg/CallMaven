import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(recipent, subject, body):
    sender_email = os.getenv("SMTP_MAIL")
    recipient_email = recipent
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMPT_PORT")
    username = os.getenv("SMTP_MAIL")
    password = os.getenv("SMTP_PASSWORD")

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as smtp_obj: # type: ignore
        smtp_obj.starttls()
        smtp_obj.login(username, password) # type: ignore
        smtp_obj.sendmail(sender_email, recipient_email, message.as_string()) # type: ignore
