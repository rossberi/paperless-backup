import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.log import log_msg


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
    
    # Validate security option
    if security not in ["ssl", "starttls", "plain"]:
        log_msg(f"ERROR - Unknown SMTP security option: {security}")
        return False
    
    try:
        # Build email message
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        log_msg(f"Sending email to {recipient} via {smtp_server}:{smtp_port} ({security})...")
        
        # Send email based on security type
        if security == "ssl":
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.login(username, password)
                server.send_message(msg)
        
        elif security == "starttls":
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(username, password)
                server.send_message(msg)
        
        elif security == "plain":
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.login(username, password)
                server.send_message(msg)
        
        log_msg("Email sent successfully")
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        log_msg(f"ERROR - SMTP authentication failed: {str(e)}")
        return False
    
    except smtplib.SMTPException as e:
        log_msg(f"ERROR - SMTP error occurred: {str(e)}")
        return False
    
    except socket.timeout:
        log_msg(f"ERROR - SMTP connection timeout ({smtp_server}:{smtp_port})")
        return False
    
    except socket.gaierror:
        log_msg(f"ERROR - Could not resolve SMTP server: {smtp_server}")
        return False
    
    except ConnectionRefusedError:
        log_msg(f"ERROR - SMTP server refused connection: {smtp_server}:{smtp_port}")
        return False
    
    except Exception as e:
        log_msg(f"ERROR - Unexpected error while sending email: {type(e).__name__}: {str(e)}")
        return False