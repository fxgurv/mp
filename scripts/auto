#!/usr/bin/env bash

# Script to generate & Upload videos to YT Shorts for all accounts in a loop

# Normalize line endings
sed -i.bak 's/\r$//' "$0" && rm "$0.bak"

# Check which interpreter to use (python)
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python not found. Please install Python 3."
  exit 1
fi

# Function to display countdown timer
countdown() {
    local seconds=$1
    while [ $seconds -gt 0 ]; do
        printf "\rNext cycle starts in: %02d:%02d:%02d" $((seconds/3600)) $(((seconds%3600)/60)) $((seconds%60))
        sleep 1
        ((seconds--))
    done
    printf "\n"
}

# Main loop
while true; do
    # Read .mp/youtube.json file, get all account IDs
    youtube_ids=$($PYTHON -c "import json; print('\n'.join([account['id'] for account in json.load(open('.mp/youtube.json'))['accounts']]))")

    echo "Starting video generation and upload cycle for all accounts"

    # Loop through each account ID
    for id in $youtube_ids; do
        echo "Processing account ID: $id"
        
        # Run python script for video generation and upload
        $PYTHON src/cron.py youtube "$id"
        
        echo "Completed processing for account ID: $id"
        echo "-------------------------------------------"
    done

    echo "All accounts processed. Starting countdown for next cycle."
    countdown 600  # 10 minutes countdown
done
