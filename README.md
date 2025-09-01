# Discord Bot

A performant Discord bot using Python and discord.py, ready for Docker deployment.

## Features
- Basic bot setup with modular structure
- Loads token from environment
- Responds to simple commands
- Dockerized for easy deployment
- Volume mapping for live code editing

## Project Structure
```
discordbot/
├── bot/                    # Bot source code (volume mapped)
│   ├── bot.py             # Main bot file
│   └── requirements.txt   # Python dependencies
├── data/                  # Persistent data storage (volume mapped)
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker build configuration
├── .env.example          # Environment variables template
└── README.md
```

## Getting Started

1. Clone the repository.
2. Add your bot token to a `.env` file:
   ```env
   DISCORD_TOKEN=your_token_here
   ```
3. Build and run with Docker:
   ```bash
   docker build -t discordbot .
   docker run --env-file .env -v ./bot:/app/bot discordbot
   ```

## Development

The `bot/` folder is mapped as a volume, so you can:
- Edit `bot.py` and see changes immediately (requires container restart)
- Add new Python files for commands and cogs
- Modify `requirements.txt` to add new dependencies (requires rebuild)
- Store persistent data in the `data/` folder

To add new commands or cogs:
1. Create new `.py` files in the `bot/` folder
2. Import and load them in `bot.py`
3. Restart the container: `docker-compose restart`

## Requirements
See `bot/requirements.txt` for Python dependencies.

## Extra Features
- Uses `python-dotenv` for environment variable management
- Responds to `!ping` with `Pong!`
- Logs bot startup
