import smtplib

from email.message import EmailMessage


def email(recipient, subject, content):
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = subject
    message["From"] = "admin@spot.com"
    message["To"] = recipient

    smtp_server = smtplib.SMTP("127.0.0.1:25")
    smtp_server.send_message(message)
    smtp_server.quit()
