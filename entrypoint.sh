#!/bin/bash

# Create the mounted directories if they don't exist
mkdir -p /app/bot-volume
mkdir -p /app/data

# Function to check if a directory is empty or doesn't exist
is_directory_empty_or_missing() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        return 0  # Directory doesn't exist
    elif [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        return 0  # Directory is empty
    else
        return 1  # Directory exists and has content
    fi
}

# Check if both bot and data directories are empty or don't exist
if is_directory_empty_or_missing "/app/bot-volume" && is_directory_empty_or_missing "/app/data"; then
    echo "Both bot and data directories are empty or don't exist. Copying default files..."
    
    # Copy default bot files
    echo "Copying default bot.py to volume..."
    cp /app/bot-default/bot.py /app/bot-volume/
    
    echo "Copying default requirements.txt to volume..."
    cp /app/bot-default/requirements.txt /app/bot-volume/
    
    echo "Copying default example_commands.py to volume..."
    cp /app/bot-default/example_commands.py /app/bot-volume/
    
    # Copy logging directory
    if [ -d "/app/bot-default/bot_logging" ]; then
        echo "Copying default bot_logging directory to volume..."
        cp -r /app/bot-default/bot_logging /app/bot-volume/
    fi
    
    # Copy any other .py files from default
    for file in /app/bot-default/*.py; do
        filename=$(basename "$file")
        if [ ! -f "/app/bot-volume/$filename" ]; then
            echo "Copying default $filename to volume..."
            cp "$file" "/app/bot-volume/"
        fi
    done
    
    echo "Default files copied successfully."
else
    echo "Bot or data directory already contains files. Skipping default file copy."
    echo "Bot directory status: $([ -d "/app/bot-volume" ] && [ -n "$(ls -A /app/bot-volume 2>/dev/null)" ] && echo "has files" || echo "empty/missing")"
    echo "Data directory status: $([ -d "/app/data" ] && [ -n "$(ls -A /app/data 2>/dev/null)" ] && echo "has files" || echo "empty/missing")"
fi

# Install/update requirements if requirements.txt exists
if [ -f "/app/bot-volume/requirements.txt" ]; then
    echo "Installing/updating Python packages..."
    pip install --no-cache-dir -r /app/bot-volume/requirements.txt
fi

echo "Starting bot..."
echo "Bot files in volume:"
ls -la /app/bot-volume/
echo "Running: python /app/bot-volume/bot.py"
# Run the bot from the volume
exec python -u /app/bot-volume/bot.py
