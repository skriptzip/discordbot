"""
Colored logging formatter for console output.

This module provides colorized log output for better readability in development
and debugging scenarios.
"""

import logging
import os
import sys
from typing import Dict


class ColoredFormatter(logging.Formatter):
    """Custom formatter adding colors to console log output."""
    
    # ANSI color codes
    COLORS = {
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        
        # Foreground colors
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        
        # Bright foreground colors
        'BRIGHT_RED': '\033[91m',
        'BRIGHT_GREEN': '\033[92m',
        'BRIGHT_YELLOW': '\033[93m',
        'BRIGHT_BLUE': '\033[94m',
        'BRIGHT_MAGENTA': '\033[95m',
        'BRIGHT_CYAN': '\033[96m',
        'BRIGHT_WHITE': '\033[97m',
    }
    
    # Level-specific color mapping
    LEVEL_COLORS = {
        logging.DEBUG: COLORS['DIM'] + COLORS['CYAN'],
        logging.INFO: COLORS['GREEN'],
        logging.WARNING: COLORS['YELLOW'],
        logging.ERROR: COLORS['RED'],
        logging.CRITICAL: COLORS['BOLD'] + COLORS['BRIGHT_RED'],
    }
    
    # Logger-specific color mapping for better organization
    LOGGER_COLORS = {
        'discord': COLORS['BLUE'],
        'discord.http': COLORS['DIM'] + COLORS['BLUE'],
        'discord.gateway': COLORS['MAGENTA'],
        'bot': COLORS['BRIGHT_GREEN'],
        'bot.commands': COLORS['CYAN'],
        'bot.events': COLORS['BRIGHT_CYAN'],
    }
    
    def __init__(self, fmt: str, datefmt: str = None, style: str = '%'):
        """
        Initialize the colored formatter.
        
        Args:
            fmt: Log format string
            datefmt: Date format string
            style: Format style ('% ', '{', or '$')
        """
        super().__init__(fmt, datefmt, style)
        
        # Check if we should use colors (disable in non-TTY environments)
        self.use_colors = self._should_use_colors()
    
    def _should_use_colors(self) -> bool:
        """
        Determine if colors should be used based on environment.
        
        Returns:
            True if colors should be used, False otherwise
        """
        # Check for explicit color forcing via environment variables
        if os.environ.get('FORCE_COLOR', '').strip():
            return True
        
        if os.environ.get('NO_COLOR', '').strip():
            return False
        
        # Disable colors if output is not a TTY (e.g., redirected to file)
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False
        
        # Enable colors if TERM suggests color support
        term = os.environ.get('TERM', '')
        if any(color_term in term for color_term in ['color', 'xterm', 'screen', 'tmux']):
            return True
        
        # Disable colors on Windows unless explicitly enabled
        if sys.platform == 'win32':
            # Enable colors if Windows Terminal or ConEmu is detected
            return any(term in term.lower() 
                      for term in ['xterm', 'color', 'ansi'])
        
        # Enable colors on Unix-like systems by default
        return True
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors if enabled.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted log message with colors
        """
        if not self.use_colors:
            return super().format(record)
        
        # Save original values
        original_levelname = record.levelname
        original_name = record.name
        
        # Apply colors
        level_color = self.LEVEL_COLORS.get(record.levelno, self.COLORS['WHITE'])
        logger_color = self._get_logger_color(record.name)
        
        # Colorize level name
        record.levelname = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
        
        # Colorize logger name
        record.name = f"{logger_color}{record.name}{self.COLORS['RESET']}"
        
        # Format the message
        formatted = super().format(record)
        
        # Restore original values
        record.levelname = original_levelname
        record.name = original_name
        
        return formatted
    
    def _get_logger_color(self, logger_name: str) -> str:
        """
        Get the appropriate color for a logger name.
        
        Args:
            logger_name: Name of the logger
            
        Returns:
            ANSI color code string
        """
        # Check for exact matches first
        if logger_name in self.LOGGER_COLORS:
            return self.LOGGER_COLORS[logger_name]
        
        # Check for partial matches (e.g., 'bot.commands' matches 'bot')
        for name_pattern, color in self.LOGGER_COLORS.items():
            if logger_name.startswith(name_pattern):
                return color
        
        # Default color for unknown loggers
        return self.COLORS['WHITE']


def create_colored_formatter(fmt: str, datefmt: str = None, style: str = '{', force_colors: bool = None) -> logging.Formatter:
    """
    Create a colored formatter instance.
    
    Args:
        fmt: Log format string
        datefmt: Date format string
        style: Format style
        force_colors: Force enable/disable colors (overrides auto-detection)
        
    Returns:
        Colored formatter instance if colors are supported, regular formatter otherwise
    """
    try:
        formatter = ColoredFormatter(fmt, datefmt, style)
        
        # Override color detection if specified
        if force_colors is not None:
            formatter.use_colors = force_colors
            
        return formatter
    except Exception:
        # Fallback to regular formatter if colored formatter fails
        return logging.Formatter(fmt, datefmt, style)
