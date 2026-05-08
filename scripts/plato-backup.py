#!/usr/bin/env python3
"""
PLATO Room Server Backup Script
Backs up all rooms from PLATO server to /tmp/plato-backup/{date}/{room_name}.json
Keeps last 48 backups (12 hours at 15-min intervals), auto-prunes older.
"""
import json
import os
import sys
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

PLATO_URL = "http://localhost:8847"
BACKUP_DIR = Path("/tmp/plato-backup")
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/repos/superinstance/scripts/plato-backup-state.json")
LOG_FILE = Path("/tmp/plato-backup.log")
MAX_BACKUPS = 48
RATE_LIMIT_MS = 50


def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def get_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"rooms": {}, "last_full_backup": None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_all_rooms():
    try:
        r = requests.get(f"{PLATO_URL}/rooms", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"ERROR: Failed to get room list: {e}")
        return []


def backup_room(room_name):
    try:
        r = requests.get(f"{PLATO_URL}/room/{room_name}", timeout=30)
        r.raise_for_status()
        data = r.json()
        tiles = data.get("tiles", [])
        return {
            "room": room_name,
            "backup_at": datetime.utcnow().isoformat(),
            "tiles": tiles
        }
    except Exception as e:
        log(f"ERROR: Failed to backup room {room_name}: {e}")
        return None


def prune_old_backups(backup_dir, date_str):
    """Remove backups older than date_str (keep date_str itself)."""
    if not backup_dir.exists():
        return
    for d in backup_dir.iterdir():
        if d.is_dir() and d.name < date_str:
            import shutil
            log(f"PRUNE: Removing old backup directory {d}")
            shutil.rmtree(d)


def prune_excess_backups(backup_dir):
    """Keep only last MAX_BACKUPS date directories."""
    if not backup_dir.exists():
        return
    dates = sorted([d.name for d in backup_dir.iterdir() if d.is_dir()], reverse=True)
    if len(dates) > MAX_BACKUPS:
        for old_date in dates[MAX_BACKUPS:]:
            import shutil
            old_path = backup_dir / old_date
            log(f"PRUNE: Removing excess backup {old_path}")
            shutil.rmtree(old_path)


def main():
    log("START: PLATO backup begins")
    state = get_state()
    backup_date = datetime.utcnow().strftime("%Y-%m-%d")
    backup_path = BACKUP_DIR / backup_date
    backup_path.mkdir(parents=True, exist_ok=True)

    rooms = get_all_rooms()
    if not rooms:
        log("WARN: No rooms found, aborting backup")
        sys.exit(1)

    log(f"Found {len(rooms)} rooms to backup")

    success_count = 0
    fail_count = 0
    now = datetime.utcnow().isoformat()

    for room_name in rooms:
        log(f"Backing up room: {room_name}")
        backup = backup_room(room_name)
        if backup:
            room_file = backup_path / f"{room_name}.json"
            with open(room_file, "w") as f:
                json.dump(backup, f)
            state["rooms"][room_name] = {
                "last_backup": now,
                "backup_date": backup_date,
                "tile_count": len(backup["tiles"])
            }
            success_count += 1
        else:
            fail_count += 1
        time.sleep(RATE_LIMIT_MS / 1000.0)

    state["last_full_backup"] = now
    save_state(state)

    # Prune old backups
    prune_old_backups(BACKUP_DIR, backup_date)
    prune_excess_backups(BACKUP_DIR)

    log(f"COMPLETE: {success_count} rooms backed up, {fail_count} failed")
    print(f"Backup complete: {success_count} success, {fail_count} failed")


if __name__ == "__main__":
    main()
