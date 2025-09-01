"""
Logging configuration for the Discord bot.

This file contains all logging-related settings and can be easily modified
to change logging behavior without touching the main bot code.
"""

import logging
from typing import Dict, Any

# Logging levels for different components
LOGGING_CONFIG: Dict[str, Any] = {
    # Main loggers and their levels
    "loggers": {
        "discord": logging.DEBUG,
        "discord.http": logging.INFO,  # Reduce HTTP request noise
        "bot": logging.INFO,
        "bot.commands": logging.INFO,
        "bot.events": logging.DEBUG,
    },
    
    # File logging settings
    "files": {
        "discord": {
            "filename": "/app/data/logs/discord.log",
            "max_bytes": 32 * 1024 * 1024,  # 32 MiB
            "backup_count": 5,
        },
        "bot": {
            "filename": "/app/data/logs/bot.log",
            "max_bytes": 16 * 1024 * 1024,  # 16 MiB
            "backup_count": 3,
        }
    },
    
    # Console logging settings
    "console": {
        "enabled": True,
        "level": logging.INFO,
        "format": "{asctime} | {levelname:<8} | {name:<20} | {message}",
        "date_format": "%H:%M:%S",
        "style": "{"
    },
    
    # File logging format
    "file_format": {
        "format": "[{asctime}] [{levelname:<8}] {name}: {message}",
        "date_format": "%Y-%m-%d %H:%M:%S",
        "style": "{"
    }
}

# Quick settings for different environments
ENVIRONMENT_CONFIGS = {
    "development": {
        "console_level": logging.DEBUG,
        "file_level": logging.DEBUG,
        "discord_http_level": logging.DEBUG,
        "colored_logs": True,
    },
    "production": {
        "console_level": logging.INFO,
        "file_level": logging.INFO,
        "discord_http_level": logging.WARNING,
        "colored_logs": True,
    },
    "minimal": {
        "console_level": logging.WARNING,
        "file_level": logging.INFO,
        "discord_http_level": logging.ERROR,
        "colored_logs": False,
    }
}

def get_environment_config(env: str = "production") -> Dict[str, Any]:
    """Get logging configuration for a specific environment."""
    return ENVIRONMENT_CONFIGS.get(env, ENVIRONMENT_CONFIGS["production"])
