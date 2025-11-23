import docker
import datetime
import os
import shutil

from app.log import log_msg

def export_paperless(container_name: str, paperless_export_dir: str, timestamp: str):
    client = docker.from_env()
    paperless = client.containers.get(container_name)
    export_cmd = f"document_exporter -z -zn backup_{timestamp} {paperless_export_dir}"
    exec_result = paperless.exec_run(export_cmd, stdout=True, stderr=True)
    log_output = exec_result.output.decode("utf-8")
    log_msg("")
    log_msg("Paperless export command executed:")
    log_msg(f"Paperless export command: {export_cmd}")
    log_msg("")
    log_msg("Paperless export output:")
    log_msg(log_output)
    log_msg("")

    if exec_result.exit_code != 0:
        raise Exception(f"ERROR - Failed to export documents. Exit-Code: {exec_result.exit_code}")

def copy_exported_zip(timestamp: str, paperless_export_dir: str, paperless_backup_dir: str):
    exported_zip = f'{paperless_export_dir}/backup_{timestamp}.zip'

    if not os.path.exists(exported_zip):
        raise FileNotFoundError(f"ERROR - Export failed – File not found: {exported_zip}")
    shutil.move(exported_zip, f'{paperless_backup_dir}/backup_{timestamp}.zip')

    log_msg(f"Created backup: backup_{timestamp}.zip | Size: {(os.path.getsize(f'{paperless_backup_dir}/backup_{timestamp}.zip')) / 1024 / 1024 / 1024} GB")
    log_msg("")

def start_backup(container_name: str, paperless_export_dir: str,backup_dir: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_msg("Paperless export started ...")
    export_paperless(container_name, paperless_export_dir, timestamp)

    log_msg("Copying exported zip ...")
    copy_exported_zip(timestamp, paperless_export_dir, backup_dir)