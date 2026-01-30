#!/bin/bash
# Usage: bash run_random_jira_comment.sh

# Set your project directory where venv and the script live:
PROJECT_DIR="/home/zzhou/code"
LOG_FILE="$PROJECT_DIR/jira_automation.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "==== Starting Jira Automation ===="

cd "$PROJECT_DIR" || { log "Project directory not found! Exiting."; exit 1; }

# Activate venv
if [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
    log "Virtual environment activated."
else
    log "Virtual environment not found! Exiting."
    exit 1
fi

# Optional: Random sleep between 0 and 2 hours (0 to 7200 seconds)
# RANDOM_DELAY=$(( RANDOM % 7200 ))
# log "Sleeping for $RANDOM_DELAY seconds before running Jira automation..."
# sleep $RANDOM_DELAY

log "Running Python Jira automation script..."
python "$PROJECT_DIR/jira_auto_comment.py" >> "$LOG_FILE" 2>&1
PY_EXIT_CODE=$?

if [ $PY_EXIT_CODE -eq 0 ]; then
    log "Jira automation script completed successfully."
else
    log "Jira automation script failed with exit code $PY_EXIT_CODE."
fi

log "==== Jira Automation Finished ===="