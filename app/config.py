import os

class Config:
    # Paperless
    PAPERLESS_CONTAINER_NAME = os.getenv("PAPERLESS_CONTAINER_NAME", "paperless")
    PAPERLESS_EXPORT_DIR = os.getenv("PAPERLESS_EXPORT_DIR", "../export")
    
    # Backup
    BACKUP_DIR = os.getenv("BACKUP_DIR", "/backup")
    EXPORT_DIR = os.getenv("EXPORT_DIR", "/export")
    KEEP_BACKUPS = int(os.getenv("KEEP_BACKUPS", "7"))
    BACKUP_PREFIX = os.getenv("BACKUP_PREFIX", "backup")
    BACKUP_ON_STARTUP = os.getenv("BACKUP_ON_STARTUP", "False")
    BACKUP_ENCRYPTION_PASSWORD = os.getenv("BACKUP_ENCRYPTION_PASSWORD")
    
    # SMTP
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER = os.getenv("SMTP_SENDER")
    SMTP_RECIPIENT = os.getenv("SMTP_RECIPIENT")
    SMTP_SUBJECT_SUCCESS = os.getenv("SMTP_SUBJECT_SUCCESS", "Paperless backup successful")
    SMTP_SUBJECT_FAILURE = os.getenv("SMTP_SUBJECT_FAILURE", "Paperless backup failed")
    SMTP_SECURITY = os.getenv("SMTP_SECURITY", "starttls")
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not os.path.exists(Config.BACKUP_DIR):
            raise FileNotFoundError(f"ERROR - Backup directory not found: {Config.BACKUP_DIR}")
        
        if not os.path.exists(Config.EXPORT_DIR):
            raise FileNotFoundError(f"ERROR - Paperless export directory not found: {Config.EXPORT_DIR}")
        
        if Config.SMTP_SERVER is not None:
            if not all([Config.SMTP_USERNAME, Config.SMTP_PASSWORD, Config.SMTP_SENDER, Config.SMTP_RECIPIENT]):
                raise ValueError("ERROR - SMTP configuration is incomplete. Please set SMTP_USERNAME, SMTP_PASSWORD, SMTP_SENDER, and SMTP_RECIPIENT environment variables.")