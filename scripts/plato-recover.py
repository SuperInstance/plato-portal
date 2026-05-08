#!/usr/bin/env python3
"""
PLATO Room Server Recovery Script
Restores room data from backup files.
"""
import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

PLATO_URL = "http://localhost:8847"
BACKUP_DIR = Path("/tmp/plato-backup")


def get_backups_for_date(date_str):
    """List all room backup files for a given date."""
    date_dir = BACKUP_DIR / date_str
    if not date_dir.exists():
        return []
    return [f for f in date_dir.iterdir() if f.suffix == ".json"]


def get_latest_backup_date():
    """Find the most recent backup date directory."""
    if not BACKUP_DIR.exists():
        return None
    dates = sorted([d.name for d in BACKUP_DIR.iterdir() if d.is_dir()], reverse=True)
    return dates[0] if dates else None


def get_existing_tile_hashes(room_name):
    """Fetch existing tile hashes from PLATO to avoid duplicates."""
    try:
        r = requests.get(f"{PLATO_URL}/room/{room_name}", timeout=30)
        r.raise_for_status()
        data = r.json()
        hashes = set()
        for t in data.get("tiles", []):
            h = t.get("tile_hash") or t.get("_hash")
            if h:
                hashes.add(h)
        return hashes
    except Exception:
        return set()


def recover_room(room_name, backup_file, skip_duplicates=True):
    """POST tiles from backup file to PLATO."""
    with open(backup_file) as f:
        backup = json.load(f)

    tiles = backup.get("tiles", [])
    if not tiles:
        return {"recovered": 0, "skipped": 0, "failed": 0, "errors": []}

    existing_hashes = set()
    if skip_duplicates:
        existing_hashes = get_existing_tile_hashes(room_name)

    recovered = 0
    skipped = 0
    failed = 0
    errors = []

    for tile in tiles:
        tile_hash = tile.get("tile_hash") or tile.get("_hash")
        if skip_duplicates and tile_hash and tile_hash in existing_hashes:
            skipped += 1
            continue

        try:
            r = requests.post(
                f"{PLATO_URL}/room/{room_name}/submit",
                json=tile,
                timeout=10
            )
            if r.status_code in (200, 201):
                recovered += 1
                if tile_hash:
                    existing_hashes.add(tile_hash)
            else:
                failed += 1
                errors.append(f"{room_name}/{tile_hash}: HTTP {r.status_code}")
        except Exception as e:
            failed += 1
            errors.append(f"{room_name}/{tile_hash}: {e}")

    return {"recovered": recovered, "skipped": skipped, "failed": failed, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Recover PLATO room data from backup")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--latest", action="store_true", help="Restore from most recent backup")
    group.add_argument("--date", help="Restore from specific date (YYYY-MM-DD)")
    parser.add_argument("--no-skip", action="store_true", help="Don't skip duplicate tiles")
    args = parser.parse_args()

    if args.latest:
        date_str = get_latest_backup_date()
        if not date_str:
            print("ERROR: No backups found")
            sys.exit(1)
        print(f"Recovering from latest backup: {date_str}")
    else:
        date_str = args.date

    backup_files = get_backups_for_date(date_str)
    if not backup_files:
        print(f"ERROR: No backup files found for date {date_str}")
        sys.exit(1)

    print(f"Found {len(backup_files)} rooms to recover from {date_str}")

    total_recovered = 0
    total_skipped = 0
    total_failed = 0
    all_errors = []

    for bf in sorted(backup_files):
        room_name = bf.stem
        print(f"Recovering room: {room_name}...")
        result = recover_room(room_name, bf, skip_duplicates=not args.no_skip)
        total_recovered += result["recovered"]
        total_skipped += result["skipped"]
        total_failed += result["failed"]
        all_errors.extend(result["errors"])
        print(f"  recovered={result['recovered']}, skipped={result['skipped']}, failed={result['failed']}")

    print(f"\n=== Recovery Summary ===")
    print(f"Date: {date_str}")
    print(f"Rooms processed: {len(backup_files)}")
    print(f"Tiles recovered: {total_recovered}")
    print(f"Tiles skipped (duplicates): {total_skipped}")
    print(f"Tiles failed: {total_failed}")

    if all_errors:
        print(f"\nErrors ({len(all_errors)}):")
        for e in all_errors[:20]:
            print(f"  {e}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")


if __name__ == "__main__":
    main()
