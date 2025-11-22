import docker
import datetime
import os
import shutil

client = docker.from_env()

container_name = os.getenv("PAPERLESS_CONTAINER_NAME", "paperless")
paperless_export_dir = os.getenv("PAPERLESS_EXPORT_DIR", "../export/")
keep_backups = os.getenv("KEEP_BACKUPS", 3)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

backup_dir = f"/app/backup"
os.makedirs(backup_dir, exist_ok=True)

print("📦 Starte Paperless Export ...")
paperless = client.containers.get(container_name)

export_cmd = f"document_exporter -z -zn backup_{timestamp} {paperless_export_dir}"
paperless.exec_run(export_cmd)

print("📥 Kopiere Dokumente ...")
shutil.move(f'/app/export/backup_{timestamp}.zip', f'{backup_dir}/backup_{timestamp}.zip')


if keep_backups > 0:
    backups = [f for f in os.listdir(backup_dir) if f.startswith("backup_") and f.endswith(".zip")]
    backups.sort()

    if len(backups) > keep_backups:
        print(f"ℹ️ Lösche alte Backups > {keep_backups} Versionen ...")
        to_delete = backups[:-keep_backups]
        for backup_file in to_delete:
            os.remove(os.path.join(backup_dir, backup_file))
            print(f"🗑️ {backup_file} gelöscht")

print(f"✅ Fertig! Backup gespeichert unter: {backup_dir}")
