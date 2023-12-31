import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_via_smtp(receiver_email, subject, body):
    smtp_server = 'smtp.meta.ua'
    smtp_port = 465
    username = "fastapi@meta.ua"
    password = "pythonCourse2023"

    message = MIMEMultipart()
    message["From"] = username
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(username, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
