"""
Logging utilities for the Discord bot.

This module provides helper functions and utilities for consistent logging
across all bot modules and cogs.
"""

import logging
import functools
from typing import Any, Callable


def get_bot_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance for bot modules.
    
    Args:
        name: Optional logger name. If not provided, uses the calling module's name.
    
    Returns:
        Configured logger instance
    """
    if name is None:
        # Get the caller's module name
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'bot')
    
    # Ensure the logger name starts with 'bot.'
    if not name.startswith('bot.'):
        name = f'bot.{name}'
        
    return logging.getLogger(name)


def log_slash_command_usage(func: Callable) -> Callable:
    """
    Decorator to automatically log slash command usage.
    
    Usage:
        @bot.tree.command()
        @log_slash_command_usage
        async def my_command(interaction):
            # Command logic here
            pass
    """
    @functools.wraps(func)
    async def wrapper(interaction, *args, **kwargs):
        logger = get_bot_logger('commands')
        
        # Log command invocation
        guild_info = f" in {interaction.guild.name}" if interaction.guild else " in DM"
        logger.info(f'Slash command "/{interaction.command.name}" invoked by {interaction.user}{guild_info}')
        
        try:
            result = await func(interaction, *args, **kwargs)
            logger.debug(f'Slash command "/{interaction.command.name}" completed successfully')
            return result
        except Exception as e:
            logger.error(f'Slash command "/{interaction.command.name}" failed: {e}', exc_info=True)
            raise
    
    return wrapper


def log_command_usage(func: Callable) -> Callable:
    """
    Decorator to automatically log traditional command usage.
    
    Usage:
        @bot.command()
        @log_command_usage
        async def my_command(ctx):
            # Command logic here
            pass
    """
    @functools.wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        logger = get_bot_logger('commands')
        
        # Log command invocation
        guild_info = f" in {ctx.guild.name}" if ctx.guild else " in DM"
        logger.info(f'Command "{ctx.command}" invoked by {ctx.author}{guild_info}')
        
        try:
            result = await func(ctx, *args, **kwargs)
            logger.debug(f'Command "{ctx.command}" completed successfully')
            return result
        except Exception as e:
            logger.error(f'Command "{ctx.command}" failed: {e}', exc_info=True)
            raise
    
    return wrapper


def log_event(event_name: str):
    """
    Decorator to log bot events.
    
    Usage:
        @bot.event
        @log_event("member_join")
        async def on_member_join(member):
            # Event logic here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = get_bot_logger('events')
            logger.debug(f'Event "{event_name}" triggered')
            
            try:
                result = await func(*args, **kwargs)
                logger.debug(f'Event "{event_name}" processed successfully')
                return result
            except Exception as e:
                logger.error(f'Event "{event_name}" failed: {e}', exc_info=True)
                raise
        
        return wrapper
    return decorator


# Quick logging functions
def log_info(message: str, module: str = None):
    """Quick logging function for info messages."""
    logger = get_bot_logger(module)
    logger.info(message)


def log_warning(message: str, module: str = None):
    """Quick logging function for warning messages."""
    logger = get_bot_logger(module)
    logger.warning(message)


def log_error(message: str, module: str = None, exc_info: bool = False):
    """Quick logging function for error messages."""
    logger = get_bot_logger(module)
    logger.error(message, exc_info=exc_info)
