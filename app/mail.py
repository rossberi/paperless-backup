import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(
    smtp_server,
    smtp_port,
    username,
    password,
    sender,
    recipient,
    subject,
    body,
    security="starttls",   # "ssl", "starttls", "plain"
):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # SSL / TLS
    if security == "ssl":
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.send_message(msg)
    
    elif security == "starttls":
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.send_message(msg)

    elif security == "plain":
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.send_message(msg)

    else:
        raise ValueError(f"Unknown security option: {security}")
