# Discord Bot

A performant Discord bot using Python and discord.py, ready for Docker deployment.

## Features
- Basic bot setup
- Loads token from environment
- Responds to simple commands
- Dockerized for easy deployment

## Getting Started

1. Clone the repository.
2. Add your bot token to a `.env` file:
   ```env
   DISCORD_TOKEN=your_token_here
   ```
3. Build and run with Docker:
   ```bash
   docker build -t discordbot .
   docker run --env-file .env discordbot
   ```

## Requirements
See `requirements.txt`.

## Extra Features
- Uses `python-dotenv` for environment variable management
- Responds to `!ping` with `Pong!`
- Logs bot startup
