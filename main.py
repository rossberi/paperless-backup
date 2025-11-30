import os

from app.backup import start_backup
from app.retentionpolicy import retention_policy
from app.mail import send_mail
from app.log import log_msg, log
from app.config import Config

success = True

Config.validate()

try:
    #start backup process
    log_msg(f"Paperless Backup started ...")
    start_backup(container_name=Config.PAPERLESS_CONTAINER_NAME, paperless_export_dir=Config.PAPERLESS_EXPORT_DIR, backup_dir=Config.BACKUP_DIR, backup_prefix=Config.BACKUP_PREFIX)

    #start retention policy
    retention_policy(keep_backups=Config.KEEP_BACKUPS, backup_dir=Config.BACKUP_DIR, backup_prefix=Config.BACKUP_PREFIX)
except Exception as e:
    log_msg(str(e))
    success = False

# Send mail with log
subject = Config.SMTP_SUBJECT_SUCCESS if success else Config.SMTP_SUBJECT_FAILURE
mail_body = "\n".join(log)

if Config.SMTP_SERVER is not None:
    send_mail(
        Config.SMTP_SERVER,
        Config.SMTP_PORT,
        Config.SMTP_USERNAME,
        Config.SMTP_PASSWORD,
        Config.SMTP_SENDER,
        Config.SMTP_RECIPIENT,
        subject,
        mail_body,
        Config.SMTP_SECURITY,
    )
else:
    log_msg("No SMTP_SERVER configured, skipping email notification")