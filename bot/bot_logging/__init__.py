"""
Comprehensive logging setup for the Discord bot.

This module handles all logging configuration and setup based on discord.py
logging recommendations and best practices.
"""

import os
import logging
import logging.handlers
import sys
from typing import Optional
from .config import LOGGING_CONFIG, get_environment_config
from .colored import create_colored_formatter


def setup_logging(environment: str = "production") -> logging.Logger:
    """
    Set up comprehensive logging for the Discord bot.
    
    Args:
        environment: Logging environment ('development', 'production', 'minimal')
        
    Returns:
        Configured bot logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('/app/data/logs', exist_ok=True)
    
    # Get environment-specific configuration
    env_config = get_environment_config(environment)
    
    # Configure loggers based on configuration
    for logger_name, level in LOGGING_CONFIG["loggers"].items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.handlers.clear()  # Clear existing handlers
    
    # Apply environment-specific overrides
    logging.getLogger('discord.http').setLevel(env_config.get('discord_http_level', logging.INFO))
    
    # Create formatters
    file_formatter = logging.Formatter(
        LOGGING_CONFIG["file_format"]["format"],
        LOGGING_CONFIG["file_format"]["date_format"],
        style='{'
    )
    
    # Create colored console formatter
    console_formatter = create_colored_formatter(
        LOGGING_CONFIG["console"]["format"],
        LOGGING_CONFIG["console"]["date_format"],
        style='{',
        force_colors=env_config.get('colored_logs', True)
    )
    
    # Set up file handlers
    for logger_name, file_config in LOGGING_CONFIG["files"].items():
        logger = logging.getLogger(logger_name)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=file_config["filename"],
            encoding='utf-8',
            maxBytes=file_config["max_bytes"],
            backupCount=file_config["backup_count"],
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(env_config.get('file_level', logging.INFO))
        logger.addHandler(file_handler)
    
    # Set up console handler if enabled
    if LOGGING_CONFIG["console"]["enabled"]:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(env_config.get('console_level', LOGGING_CONFIG["console"]["level"]))
        
        # Add console handler to main loggers
        for logger_name in ["discord", "bot"]:
            logger = logging.getLogger(logger_name)
            logger.addHandler(console_handler)
    
    # Log the logging setup
    bot_logger = logging.getLogger('bot')
    bot_logger.info('🎨 Colored logging system initialized')
    bot_logger.info(f'📊 Environment: {environment}')
    bot_logger.info(f'🖥️  Console level: {logging.getLevelName(env_config.get("console_level", logging.INFO))}')
    bot_logger.info(f'📁 File level: {logging.getLevelName(env_config.get("file_level", logging.INFO))}')
    bot_logger.info(f'🌈 Colored logs: {"enabled" if env_config.get("colored_logs", True) else "disabled"}')
    
    return bot_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for bot modules.
    
    Args:
        name: Optional logger name. If not provided, uses 'bot' as default.
        
    Returns:
        Configured logger instance
    """
    if name is None:
        name = 'bot'
    elif not name.startswith('bot.'):
        name = f'bot.{name}'
    
    return logging.getLogger(name)


def log_startup_info(logger: logging.Logger, bot_info: dict):
    """
    Log comprehensive startup information.
    
    Args:
        logger: Logger instance
        bot_info: Dictionary containing bot information
    """
    logger.info('=' * 60)
    logger.info('🤖 Discord Bot Starting Up')
    logger.info('=' * 60)
    
    for key, value in bot_info.items():
        logger.info(f'  {key}: {value}')
    
    logger.info('=' * 60)
    logger.info('🚀 Bot initialization complete!')
