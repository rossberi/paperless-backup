# 📦 Paperless Backup

An automated Docker-based backup system for [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) with email notifications and intelligent retention policies.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088F0?style=for-the-badge&logo=github-actions&logoColor=white)

## ✨ Features

- **🔄 Automated Backups** - Time-scheduled backups with cron integration
- **📧 Email Notifications** - Success and failure alerts via SMTP
- **🧹 Retention Policy** - Automatic cleanup of old backups


## 🚀 Quick Start

### Docker Run

```bash
docker run -d \
  --name paperless-backup \
  -e PAPERLESS_CONTAINER_NAME=paperless \
  -e BACKUP_SCHEDULE="0 2 * * *" \
  -e KEEP_BACKUPS=7 \
  -v /path/to/paperless/export:/paperless/export:ro \
  -v /path/to/backups:/backups \
  ghcr.io/yourusername/paperless-backup:latest
```

### Docker Compose (with SMTP)

```yaml
services:
  paperless-backup:
    image: ghcr.io/rossberi/paperless-backup:latest
    container_name: paperless-backup
    environment:
      PAPERLESS_CONTAINER_NAME: paperless
      PAPERLESS_EXPORT_DIR: '../export/'
      BACKUP_DIR: '/backups'
      EXPORT_DIR: '/export'
      BACKUP_SCHEDULE: "0 2 * * *"  # Daily at 02:00
      KEEP_BACKUPS: 7
      
      # Optional: SMTP Configuration
      # SMTP_SERVER: smtp.example.com
      # SMTP_PORT: 587
      # SMTP_USERNAME: your-email@example.com
      # SMTP_PASSWORD: your-app-password
      # SMTP_SENDER: your-email@example.com
      # SMTP_RECIPIENT: recipient@example.com
      # SMTP_SUBJECT_SUCCESS: "✅ Paperless Backup successful"
      # SMTP_SUBJECT_FAILURE: "❌ Paperless Backup failed"
      # SMTP_SECURITY: starttls
    volumes:
      - /path/to/paperless/export:/paperless/export
      - /path/to/backups:/backups
```

## 📋 Configuration

### Required Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PAPERLESS_CONTAINER_NAME` | `paperless` | Name of the Paperless Docker container |
| `PAPERLESS_EXPORT_DIR` | `../export/` | Export directory inside Paperless container |
| `BACKUP_DIR` | `/backup` | Target directory for backups |
| `EXPORT_DIR` | `/export` | Local export directory |
| `KEEP_BACKUPS` | `7` | Number of backup versions to keep |

### Optional: SMTP Configuration

To enable email notifications, set the following variables:

| Variable | Description |
|----------|-------------|
| `SMTP_SERVER` | SMTP server address |
| `SMTP_PORT` | SMTP port (default: `587`) |
| `SMTP_USERNAME` | Username for SMTP authentication |
| `SMTP_PASSWORD` | Password for SMTP authentication |
| `SMTP_SENDER` | Sender email address |
| `SMTP_RECIPIENT` | Recipient email address |
| `SMTP_SUBJECT_SUCCESS` | Subject line for successful backup |
| `SMTP_SUBJECT_FAILURE` | Subject line for failed backup |
| `SMTP_SECURITY` | Security type: `starttls` (default), `ssl`, or `plain` |

### Cron Syntax

The `BACKUP_SCHEDULE` variable uses standard cron syntax:

```
┌───────────── Minute (0 - 59)
│ ┌───────────── Hour (0 - 23)
│ │ ┌───────────── Day of Month (1 - 31)
│ │ │ ┌───────────── Month (1 - 12)
│ │ │ │ ┌───────────── Day of Week (0 - 6) (Sunday = 0)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

**Examples:**
- `0 2 * * *` - Daily at 02:00 AM
- `0 3 * * 0` - Every Sunday at 03:00 AM
- `30 1 * * *` - Daily at 01:30 AM
- `0 */4 * * *` - Every 4 hours


## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📞 Support

- 🐛 [Issues](https://github.com/yourusername/paperless-backup/issues)

## 📚 Resources

- [Paperless-ngx Documentation](https://docs.paperless-ngx.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Cron Syntax Reference](https://crontab.guru/)

---

**Note:** Make sure to regularly test your backups and keep them in a safe location! 🔒
