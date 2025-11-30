#!/usr/bin/env python3
"""Simple health check for Paperless Backup container."""

import os
import sys

def main():
    # Check backup directory
    backup_dir = os.getenv("BACKUP_DIR", "/backup")
    if not os.path.exists(backup_dir) or not os.access(backup_dir, os.W_OK):
        print(f"ERROR - Backup directory not accessible: {backup_dir}")
        return 1
    
    # Check export directory
    export_dir = os.getenv("EXPORT_DIR", "/export")
    if not os.path.exists(export_dir) or not os.access(export_dir, os.R_OK):
        print(f"ERROR - Export directory not accessible: {export_dir}")
        return 1
    
    # Check Docker socket
    if not os.path.exists("/var/run/docker.sock"):
        print("ERROR - Docker socket not found")
        return 1
    
    print("OK - Health check passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())