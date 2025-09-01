import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Import our logging system
from bot_logging import setup_logging, log_startup_info

def main():
    """Main function to run the Discord bot."""
    # Load environment variables
    load_dotenv()
    
    # Set up logging
    log_env = os.getenv('LOG_ENVIRONMENT', 'production')
    logger = setup_logging(log_env)
    
    # Get Discord token
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.critical("DISCORD_TOKEN not found in environment variables!")
        sys.exit(1)
    
    # Log startup information
    startup_info = {
        'Python Version': sys.version.split()[0],
        'discord.py Version': discord.__version__,
        'Log Environment': log_env,
        'Bot Starting': 'Initializing...'
    }
    log_startup_info(logger, startup_info)
    
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create bot instance
    bot = DiscordBot(intents=intents, logger=logger)
    
    # Register slash commands
    bot.tree.add_command(ping_slash)
    bot.tree.add_command(status_slash)
    bot.tree.add_command(info_slash)
    
    # Load example commands cog if it exists
    async def load_cogs():
        try:
            await bot.load_extension('example_commands')
            logger.info('Loaded example_commands cog')
        except ImportError:
            logger.debug('example_commands module not found, skipping')
        except Exception as e:
            logger.warning(f'Failed to load example_commands cog: {e}')
    
    # Store the cog loading function for later use
    bot._load_cogs = load_cogs
    
    try:
        # Run the bot (suppress discord.py's default logging since we have our own)
        logger.info('Starting Discord bot connection...')
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        logger.critical('Invalid Discord token provided!')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('Bot shutdown requested by user')
    except Exception as e:
        logger.critical(f'Failed to start bot: {e}', exc_info=True)
        sys.exit(1)


class DiscordBot(commands.Bot):
    """Custom Discord bot class with integrated logging."""
    
    def __init__(self, *args, logger=None, **kwargs):
        # Set a minimal command prefix since we're using slash commands
        if 'command_prefix' not in kwargs:
            kwargs['command_prefix'] = commands.when_mentioned
        super().__init__(*args, **kwargs)
        self.logger = logger or setup_logging()
        
    async def setup_hook(self):
        """This is called when the bot starts up."""
        self.logger.info('Bot setup hook called - registering slash commands')
        
        # Load cogs if the function exists
        if hasattr(self, '_load_cogs'):
            await self._load_cogs()
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            self.logger.info(f'Synced {len(synced)} slash command(s)')
        except Exception as e:
            self.logger.error(f'Failed to sync slash commands: {e}', exc_info=True)
    
    async def on_ready(self):
        """Called when the bot is ready."""
        self.logger.info(f'Bot logged in as {self.user.name} (ID: {self.user.id})')
        self.logger.info(f'Connected to {len(self.guilds)} guild(s)')
        self.logger.info(f'Monitoring {len(self.users)} users')
        self.logger.info('Bot is ready and operational!')
        
        # Set activity status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servers"
        )
        await self.change_presence(activity=activity)
        self.logger.debug('Bot presence updated')
    
    async def on_guild_join(self, guild):
        """Log when the bot joins a new guild."""
        self.logger.info(f'Bot joined new guild: {guild.name} (ID: {guild.id}) with {guild.member_count} members')
    
    async def on_guild_remove(self, guild):
        """Log when the bot leaves a guild."""
        self.logger.info(f'Bot removed from guild: {guild.name} (ID: {guild.id})')
    
    async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
        """Handle application command errors."""
        command_name = interaction.command.name if interaction.command else "unknown"
        
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            self.logger.debug(f'Command "{command_name}" on cooldown for {interaction.user}')
            await interaction.response.send_message(
                f'⏰ This command is on cooldown. Try again in {error.retry_after:.1f} seconds.',
                ephemeral=True
            )
            return
        
        if isinstance(error, discord.app_commands.MissingPermissions):
            self.logger.warning(f'User {interaction.user} missing permissions for command "{command_name}": {error.missing_permissions}')
            await interaction.response.send_message(
                f'❌ You need the following permissions: {", ".join(error.missing_permissions)}',
                ephemeral=True
            )
            return
        
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            self.logger.warning(f'Bot missing permissions for command "{command_name}": {error.missing_permissions}')
            await interaction.response.send_message(
                f'❌ I need the following permissions: {", ".join(error.missing_permissions)}',
                ephemeral=True
            )
            return
        
        # Log unexpected errors
        self.logger.error(f'Unexpected error in slash command "{command_name}" by {interaction.user}: {error}', exc_info=True)
        
        if interaction.response.is_done():
            await interaction.followup.send('❌ An unexpected error occurred. The issue has been logged.', ephemeral=True)
        else:
            await interaction.response.send_message('❌ An unexpected error occurred. The issue has been logged.', ephemeral=True)


# Create bot instance for registering commands
bot = None

def get_bot():
    """Get the bot instance."""
    return bot


# Slash Commands
@discord.app_commands.command(name="ping", description="Check bot latency and responsiveness")
async def ping_slash(interaction: discord.Interaction):
    """Check bot latency and responsiveness."""
    logger = setup_logging().getChild('commands')
    logger.info(f'Ping slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
    
    latency = round(interaction.client.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=0x00ff00
    )
    
    await interaction.response.send_message(embed=embed)
    logger.debug(f'Ping response sent with {latency}ms latency')


@discord.app_commands.command(name="status", description="Show bot status and statistics")
async def status_slash(interaction: discord.Interaction):
    """Show bot status and statistics."""
    logger = setup_logging().getChild('commands')
    logger.info(f'Status slash command invoked by {interaction.user}')
    
    bot = interaction.client
    
    embed = discord.Embed(
        title="🤖 Bot Status",
        color=0x0099ff
    )
    embed.add_field(name="🏓 Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🏠 Guilds", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Users", value=len(bot.users), inline=True)
    embed.add_field(name="📝 Slash Commands", value=len(bot.tree.get_commands()), inline=True)
    
    await interaction.response.send_message(embed=embed)


@discord.app_commands.command(name="info", description="Display bot information and help")
async def info_slash(interaction: discord.Interaction):
    """Display bot information and help."""
    logger = setup_logging().getChild('commands')
    logger.info(f'Info slash command invoked by {interaction.user}')
    
    embed = discord.Embed(
        title="ℹ️ Bot Information",
        description="A Discord bot with comprehensive logging and slash commands!",
        color=0x7289da
    )
    
    embed.add_field(
        name="📋 Available Commands",
        value="• `/ping` - Check bot latency\n• `/status` - Show bot statistics\n• `/info` - Show this information",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Features",
        value="• Slash commands\n• Comprehensive logging\n• File rotation\n• Docker support",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)


if __name__ == '__main__':
    # Run the main function
    main()
