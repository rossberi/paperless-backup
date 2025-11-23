import os

from app.backup import start_backup
from app.retentionpolicy import retention_policy
from app.mail import send_mail
from app.log import log_msg, log

success = True


#environment variables
container_name = os.getenv("PAPERLESS_CONTAINER_NAME", "paperless")
paperless_export_dir = os.getenv("PAPERLESS_EXPORT_DIR", "../export/")
keep_backups = int(os.getenv("KEEP_BACKUPS", "3"))
backup_dir = os.getenv("BACKUP_DIR", "/backup")
export_dir = os.getenv("EXPORT_DIR", "/export")

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
username = os.getenv("SMTP_USERNAME")
password = os.getenv("SMTP_PASSWORD")
sender = os.getenv("SMTP_SENDER")
recipient = os.getenv("SMTP_RECIPIENT")
subject_success = os.getenv("SMTP_SUBJECT_SUCCESS", "Paperless backup successful")
subject_failure = os.getenv("SMTP_SUBJECT_FAILURE", "Paperless backup failed")
security = os.getenv("SMTP_SECURITY", "starttls")


if smtp_server is not None:
        if username is None or password is None or sender is None or recipient is None:
                raise ValueError("ERROR - SMTP configuration is incomplete. Please set SMTP_USERNAME, SMTP_PASSWORD, SMTP_SENDER, and SMTP_RECIPIENT environment variables.")

if not os.path.exists(backup_dir):
        raise FileNotFoundError(f"ERROR - Backup directory not found: {backup_dir}")

if not os.path.exists(export_dir):
        raise FileNotFoundError(f"ERROR - Paperless export directory not found: {export_dir}")

try:
    #start backup process
    log_msg(f"Paperless Backup started ...")
    start_backup(container_name, paperless_export_dir, backup_dir)

    #start retention policy
    retention_policy(keep_backups=keep_backups, backup_dir=backup_dir)
except Exception as e:
    log_msg(str(e))
    success = False

subject = subject_success if success else subject_failure
mail_body = "\n".join(log)

if smtp_server is not None:
    send_mail(
        smtp_server,
        smtp_port,
        username,
        password,
        sender,
        recipient,
        subject,
        mail_body,
        security,
    )