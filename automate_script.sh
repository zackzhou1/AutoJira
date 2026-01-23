#!/bin/bash
# Usage: bash run_random_jira_comment.sh

# Set your project directory where venv and the script live:
PROJECT_DIR="/home/zzhou/code"

cd "$PROJECT_DIR" || { echo "Project directory not found! Exiting."; exit 1; }

# Activate venv
source "$PROJECT_DIR/venv/bin/activate"

# Random sleep between 0 and 2 hours (0 to 7200 seconds)
RANDOM_DELAY=$(( RANDOM % 7200 ))
echo "Sleeping for $RANDOM_DELAY seconds before running Jira automation..."
sleep $RANDOM_DELAY

# Run the Python automation
python "$PROJECT_DIR/jira_auto_comment.py"