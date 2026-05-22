#!/bin/bash
#===========================================================
# MySQL Backup Script for AI Interactive Drama Platform
# Usage: ./backup.sh [options]
#   -d, --dir      Backup directory (default: /www/workspace/ai-interactive-drama/backups)
#   -r, --retention Retention days (default: 7)
#   -h, --help     Show this help
#===========================================================

set -euo pipefail

# --- Config (can be overridden by env) ---
MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
MYSQL_USER="${MYSQL_USER:-aivideo}"
MYSQL_PASS="${MYSQL_PASS:-aivideo123}"
BACKUP_DIR="${BACKUP_DIR:-/www/workspace/ai-interactive-drama/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
DATABASES="${DATABASES:-ai_video}"
BACKUP_USER="${BACKUP_USER:-root}"
BACKUP_PASS="${BACKUP_PASS:-password}"

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--dir) BACKUP_DIR="$2"; shift 2 ;;
    -r|--retention) RETENTION_DAYS="$2"; shift 2 ;;
    -h|--help) grep "^#=== " "$0" | cut -c4-; exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# --- Setup ---
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/ai_drama_${TIMESTAMP}.sql.gz"
LOG_FILE="${BACKUP_DIR}/backup.log"
LOCK_FILE="${BACKUP_DIR}/.backup.lock"

mkdir -p "$BACKUP_DIR"

# --- Lock to prevent concurrent runs ---
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Backup already running, exiting" | tee -a "$LOG_FILE"
  exit 1
fi

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- Cleanup old backups ---
CUTOFF=$(date -d "$RETENTION_DAYS days ago" +%Y%m%d_%H%M%S 2>/dev/null || date -v-${RETENTION_DAYS}d +%Y%m%d_%H%M%S)
DELETED=0
for old in "${BACKUP_DIR}"/ai_drama_*.sql.gz; do
  [[ -f "$old" ]] || continue
  fname=$(basename "$old")
  # Extract timestamp from filename: ai_drama_YYYYMMDD_HHMMSS.sql.gz
  fdate="${fname#ai_drama_}"
  fdate="${fdate%.sql.gz}"
  if [[ "$fdate" < "$CUTOFF" ]]; then
    rm -f "$old"
    log "Deleted old backup: $fname"
    DELETED=$((DELETED + 1))
  fi
done
log "Cleanup: removed $DELETED old backup(s)"

log "=== Backup started ==="
log "Host: $MYSQL_HOST:$MYSQL_PORT"
log "User: $MYSQL_USER (backup user: $BACKUP_USER)"
log "Databases: $DATABASES"
log "Retention: $RETENTION_DAYS days"
log "Output: $BACKUP_FILE"

# --- Cleanup old backups ---
CUTOFF=$(date -d "$RETENTION_DAYS days ago" +%Y%m%d_%H%M%S 2>/dev/null || date -v-${RETENTION_DAYS}d +%Y%m%d_%H%M%S)
DELETED=0
for old in "${BACKUP_DIR}"/ai_drama_*.sql.gz; do
  [[ -f "$old" ]] || continue
  fname=$(basename "$old")
  # Extract timestamp from filename: ai_drama_YYYYMMDD_HHMMSS.sql.gz
  fdate="${fname#ai_drama_}"
  fdate="${fdate%.sql.gz}"
  if [[ "$fdate" < "$CUTOFF" ]]; then
    rm -f "$old"
    log "Deleted old backup: $fname"
    ((DELETED++))
  fi
done
log "Cleanup: removed $DELETED old backup(s)"

# --- Run mysqldump ---
TMP_FILE="${BACKUP_DIR}/ai_drama_${TIMESTAMP}.sql"
DUMP_OK=0

for DB in $DATABASES; do
  log "Dumping database: $DB"
  if mysqldump -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASS" \
    --single-transaction --quick --routines --triggers \
    --events --hex-blob \
    "$DB" 2>>"$LOG_FILE" | gzip > "${TMP_FILE%.sql}.${DB}.sql.gz"; then
    log "  → $DB: OK"
    DUMP_OK=$((DUMP_OK + 1))
  else
    log "  → $DB: FAILED (check $LOG_FILE)"
  fi
done

# --- Assemble final backup file ---
FINAL_FILE="${BACKUP_DIR}/ai_drama_${TIMESTAMP}.full.sql.gz"
if [[ $DUMP_OK -ne $(echo $DATABASES | wc -w) ]]; then
  log "=== Backup FAILED: some databases failed ==="
  exit 1
fi

# Count individual db files created
mapfile -t DB_FILES < <(ls "${BACKUP_DIR}"/ai_drama_"${TIMESTAMP}".*.sql.gz 2>/dev/null || true)
if [[ ${#DB_FILES[@]} -eq 0 ]]; then
  log "Backup FAILED: no dump files found"
  exit 1
fi

if [[ ${#DB_FILES[@]} -eq 1 ]]; then
  # Single DB — just rename
  mv "${DB_FILES[0]}" "$FINAL_FILE"
else
  # Multi-DB — concatenate
  cat "${DB_FILES[@]}" > "$FINAL_FILE"
  rm -f "${DB_FILES[@]}"
fi

# --- Verify gzip integrity ---
if gzip -t "$FINAL_FILE" 2>/dev/null; then
  SIZE=$(du -h "$FINAL_FILE" | cut -f1)
  MD5=$(md5sum "$FINAL_FILE" | cut -d' ' -f1)
  log "Backup complete: $FINAL_FILE ($SIZE, MD5: $MD5)"
  log "=== Backup SUCCESS ==="
  echo "SUCCESS|$FINAL_FILE|$SIZE|$MD5"
  exit 0
else
  log "Backup FAILED: compressed file integrity check failed"
  rm -f "$FINAL_FILE"
  exit 1
fi
