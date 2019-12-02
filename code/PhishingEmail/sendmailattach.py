import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 465
username = 'phishingdetective@gmail.com'
password = 'phishtooldetect97'
sender = 'phishingdetective@gmail.com'
targets = ['isaacpitblado@tamu.edu', 'isaacpitblado@gmail.com']

msg = MIMEMultipart()
msg['Subject'] = 'I have a picture'
msg['From'] = sender
msg['To'] = ', '.join(targets)

txt = MIMEText('I just bought a new camera.')
msg.attach(txt)

filepath = './rose.jpeg'
with open(filepath, 'rb') as f:
    img = MIMEImage(f.read())

img.add_header('Content-Disposition',
               'attachment',
               filename=os.path.basename(filepath))
msg.attach(img)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()