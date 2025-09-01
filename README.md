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

### How the Volume Mapping Works

This setup uses a smart volume mapping system:

1. **Default Files**: The container includes default bot files in `/app/bot-default/`
2. **Volume Mount**: Your local `bot/` folder is mounted to `/app/bot-volume/` in the container
3. **Auto-Copy**: On startup, the container automatically copies default files to the volume if they don't exist locally
4. **Live Editing**: You can edit files in your local `bot/` folder and they persist between container restarts

### First Run
When you first run `docker-compose up`, the container will:
- Create the `bot/` folder locally if it doesn't exist
- Copy `bot.py`, `requirements.txt`, and `example_commands.py` to your local `bot/` folder
- Start the bot using the files from your local folder

### Development Workflow
1. **Edit Files**: Modify files in the `bot/` folder using your favorite editor
2. **Add New Files**: Create new `.py` files for commands, cogs, or utilities
3. **Update Dependencies**: Edit `requirements.txt` to add new packages
4. **Restart**: Run `docker-compose restart` to apply changes
5. **Rebuild**: Run `docker-compose up --build` if you added new dependencies

### Adding New Commands
1. Create new `.py` files in the `bot/` folder
2. Import and load them in `bot.py`
3. Restart the container: `docker-compose restart`

Example: Uncomment the code in `example_commands.py` and add this to `bot.py`:
```python
await bot.load_extension('example_commands')
```

## Requirements
See `bot/requirements.txt` for Python dependencies.

## Extra Features
- Uses `python-dotenv` for environment variable management
- Responds to `!ping` with `Pong!`
- Logs bot startup
