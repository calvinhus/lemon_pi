import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
from soil_moisture_sensor import SoilMoistureLevel
load_dotenv()  # take environment variables from .env.

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server
SMTP_PORT = 587 #Server Port

# Credentials
SENDER = os.environ.get('SENDER_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
RECEIVER = os.environ.get('RECEIVER_EMAIL')

# image
path = "/home/pi/lemon_pi/daily_picture/"
today = datetime.now().strftime("%d-%m-%Y")
image_path = path + today + ".jpg"

# soil moisture level
_, _, soil_moisture_percentage = SoilMoistureLevel()

def SendMail(ImgFileName):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = f"Lemon Pi Watering - {today}"
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    text = MIMEText(f"Your lemon tree is healthy! Watered today. Soil moisture is at {soil_moisture_percentage}%")
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



#SendMail(image_path)
