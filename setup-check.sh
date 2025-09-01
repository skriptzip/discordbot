#!/bin/bash

echo "=== Discord Bot Setup Test ==="
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "⚠ .env file not found - copying from .env.example"
    cp .env.example .env
    echo "  Please edit .env and add your DISCORD_TOKEN"
fi

echo ""
echo "=== Project Structure ==="
echo "Current directory contents:"
ls -la

echo ""
echo "Bot folder contents:"
if [ -d "bot" ]; then
    ls -la bot/
else
    echo "Bot folder not found - will be created by Docker"
fi

echo ""
echo "To start the bot:"
echo "1. Edit .env with your Discord token"
echo "2. Run: docker-compose up -d"
echo "3. Check logs: docker-compose logs -f"
echo "4. Edit files in the bot/ folder and restart: docker-compose restart"
