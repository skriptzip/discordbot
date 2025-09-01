#!/bin/bash

# Create the mounted bot directory if it doesn't exist
mkdir -p /app/bot-volume

# Copy default bot files to the volume if they don't exist
if [ ! -f "/app/bot-volume/bot.py" ]; then
    echo "Copying default bot.py to volume..."
    cp /app/bot-default/bot.py /app/bot-volume/
fi

if [ ! -f "/app/bot-volume/requirements.txt" ]; then
    echo "Copying default requirements.txt to volume..."
    cp /app/bot-default/requirements.txt /app/bot-volume/
fi

if [ ! -f "/app/bot-volume/example_commands.py" ]; then
    echo "Copying default example_commands.py to volume..."
    cp /app/bot-default/example_commands.py /app/bot-volume/
fi

# Copy any other .py files from default if they don't exist in volume
for file in /app/bot-default/*.py; do
    filename=$(basename "$file")
    if [ ! -f "/app/bot-volume/$filename" ]; then
        echo "Copying default $filename to volume..."
        cp "$file" "/app/bot-volume/"
    fi
done

# Install/update requirements if requirements.txt was updated
if [ -f "/app/bot-volume/requirements.txt" ]; then
    echo "Installing/updating Python packages..."
    pip install --no-cache-dir -r /app/bot-volume/requirements.txt
fi

echo "Starting bot..."
# Run the bot from the volume
exec python /app/bot-volume/bot.py
