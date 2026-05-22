#!/bin/bash
#===========================================================
# MySQL Restore Script for AI Interactive Drama Platform
# Usage: ./restore.sh <backup_file> [options]
#   -f, --file     Backup .sql.gz file to restore (required)
#   -d, --database Target database (default: ai_video)
#   --dry-run      Show what would be done without executing
#   -h, --help     Show this help
#===========================================================

set -euo pipefail

# --- Config ---
MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-aivideo}"
MYSQL_PASS="${MYSQL_PASS:-aivideo123}"
TARGET_DB="${TARGET_DB:-ai_video}"

BACKUP_FILE=""
DRY_RUN=false

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case $1 in
    -f|--file) BACKUP_FILE="$2"; shift 2 ;;
    -d|--database) TARGET_DB="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) grep "^#=== " "$0" | cut -c4-; exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$BACKUP_FILE" ]]; then
  echo "ERROR: --file is required"
  echo "Usage: $0 --file <backup.sql.gz> [-d database]"
  exit 1
fi

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "ERROR: File not found: $BACKUP_FILE"
  exit 1
fi

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

log "=== Restore started ==="
log "Backup: $BACKUP_FILE"
log "Target: $TARGET_DB @ ${MYSQL_HOST}:${MYSQL_PORT}"

if $DRY_RUN; then
  log "[DRY RUN] Would execute:"
  log "  zcat $BACKUP_FILE | mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p**** $TARGET_DB"
  log "[DRY RUN] Restore skipped (dry-run mode)"
  exit 0
fi

# Verify gzip integrity
if ! gzip -t "$BACKUP_FILE" 2>/dev/null; then
  log "ERROR: Invalid gzip file: $BACKUP_FILE"
  exit 1
fi

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
MD5=$(md5sum "$BACKUP_FILE" | cut -d' ' -f1)
log "File verified: $SIZE, MD5: $MD5"

# Check available space (at least 2x file size free in /var/lib/mysql)
REQD_SPACE=$(du -sb "$BACKUP_FILE" | cut -f1)
AVAIL_SPACE=$(df -B1 /var/lib/mysql | tail -1 | awk '{print $4}')
if [[ "$AVAIL_SPACE" -lt $((REQD_SPACE * 2)) ]]; then
  log "WARNING: Low disk space. Available: $((AVAIL_SPACE / 1024 / 1024))MB, Required: $((REQD_SPACE * 2 / 1024 / 1024))MB"
fi

# Warn before drop
log "WARNING: This will DROP all existing tables in '$TARGET_DB' and replace with backup data"
log "Waiting 5 seconds... (Ctrl+C to abort)"
sleep 5

# Drop existing tables (to handle schema changes between backups)
log "Dropping existing tables..."
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" "$TARGET_DB" 2>/dev/null << 'DROPSQL'
SET FOREIGN_KEY_CHECKS=0;
SELECT CONCAT('DROP TABLE IF EXISTS `', TABLE_NAME, '`') FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() INTO @sql;
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
SET FOREIGN_KEY_CHECKS=1;
DROPSQL

log "Restoring from backup..."
if zcat "$BACKUP_FILE" | mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" "$TARGET_DB" 2>/dev/null; then
  ROWS=$(mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" "$TARGET_DB" -e "SELECT COUNT(*) as cnt FROM drama" 2>/dev/null | tail -1)
  log "=== Restore SUCCESS === (drama table: $ROWS rows)"
  exit 0
else
  log "=== Restore FAILED ==="
  exit 1
fi