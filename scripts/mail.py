import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
from scripts.soil_moisture_sensor import SoilMoistureLevel

load_dotenv()  # take environment variables from .env.

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server
SMTP_PORT = 587  # Server Port

# Credentials
SENDER = os.environ.get('SENDER_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
RECEIVER = os.environ.get('RECEIVER_EMAIL')

# soil moisture level
_, _, soil_moisture_percentage = SoilMoistureLevel()

today = datetime.now().strftime("%d-%m-%Y")


def SendMail(ImgFileName, subject):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = f"Lemon Pi Watering - {today}"
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    text = MIMEText(subject)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SENDER, PASSWORD)
    s.sendmail(SENDER, RECEIVER, msg.as_string())
    s.quit()


# SendMail(image_path)
