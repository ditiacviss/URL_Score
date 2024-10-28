import smtplib, ssl
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "diti.b@acviss.com"
context = ssl.create_default_context()

def sendmail(receiver_email, subject, message, password):
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            msg=MIMEMultipart()
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain", "utf-8"))
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)
