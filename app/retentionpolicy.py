import os
from app.log import log_msg

def retention_policy(keep_backups: int, backup_dir: str, backup_prefix: str):
    if keep_backups > 0:
        backups = [f for f in os.listdir(backup_dir) if f.startswith(f"{backup_prefix}_") and f.endswith(".zip")]
        backups.sort()
        if len(backups) > keep_backups:
            log_msg(f"Delete old backups > {keep_backups} versions ...")
            to_delete = backups[:-keep_backups]
            for backup_file in to_delete:
                os.remove(os.path.join(backup_dir, backup_file))
                log_msg(f"{backup_file} deleted")