#!/bin/bash
#===========================================================
# Cron Setup for MySQL Backup
# Usage: ./setup-cron.sh [options]
#   -u, --user     Cron user (default: developer)
#   -t, --time     Cron time (default: "3:00" = 3 AM daily)
#   --remove       Remove the cron entry
#===========================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${SCRIPT_DIR}/backup.sh"
CRON_USER="${CRON_USER:-developer}"
CRON_TIME="${CRON_TIME:-3:00}"
CRON_LINE="0 ${CRON_TIME#*:} ${CRON_TIME%%:*} * * ${BACKUP_SCRIPT} >> /www/workspace/ai-interactive-drama/backups/backup.log 2>&1"

show_help() {
  grep "^#=== " "$0" | cut -c4-
}

REMOVE=false
while [[ $# -gt 0 ]]; do
  case $1 in
    -u|--user) CRON_USER="$2"; shift 2 ;;
    -t|--time) CRON_TIME="$2"; shift 2 ;;
    --remove) REMOVE=true; shift ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

# Create backup dir (for log file)
mkdir -p /www/workspace/ai-interactive-drama/backups

if $REMOVE; then
  echo "Removing cron entry for user: $CRON_USER"
  crontab -u "$CRON_USER" -l 2>/dev/null | grep -v "backup.sh" | crontab -u "$CRON_USER" - 2>/dev/null || true
  echo "Done."
  exit 0
fi

# Build cron line
IFS=':' read -r H M <<< "$CRON_TIME"
CRON_ENTRY="$M $H * * * $BACKUP_SCRIPT >> /www/workspace/ai-interactive-drama/backups/backup.log 2>&1"

# Install
echo "Installing cron for user: $CRON_USER"
echo "Time: daily at ${CRON_TIME}"
echo "Entry: $CRON_ENTRY"

EXISTING=$(crontab -u "$CRON_USER" -l 2>/dev/null | grep -v "backup.sh" || true)
echo "$EXISTING" > /tmp/crontab_existing.txt
echo "$CRON_ENTRY" >> /tmp/crontab_existing.txt
crontab -u "$CRON_USER" /tmp/crontab_existing.txt
rm -f /tmp/crontab_existing.txt

echo ""
echo "Installed crontab:"
crontab -u "$CRON_USER" -l 2>/dev/null | grep "backup.sh" || echo "(none)"
echo ""
echo "Run backup manually:"
echo "  BACKUP_DIR=/www/workspace/ai-interactive-drama/backups $BACKUP_SCRIPT"