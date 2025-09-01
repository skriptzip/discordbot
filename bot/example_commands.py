# Example: How to add new slash commands to your bot with proper logging
# 
# This file shows how to create a cog with slash commands that can be loaded into the main bot.
# To use this example:
# 1. Uncomment the code below
# 2. In bot.py, add: await bot.load_extension('example_commands')
# 3. Restart the container

"""
import discord
from discord import app_commands
from discord.ext import commands

class ExampleSlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Get logger from the bot instance to avoid re-initialization
        self.logger = bot.logger.getChild('example_commands')
        self.logger.info("ExampleSlashCommands cog initialized")

    @app_commands.command(name='hello', description='Say hello to a user')
    async def hello_slash(self, interaction: discord.Interaction):
        '''Say hello to a user'''
        logger = self.bot.logger.getChild('commands')
        logger.debug(f"Processing hello command for user: {interaction.user}")
        logger.info(f'Hello slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
        logger.info(f"Greeting user {interaction.user.display_name}")
        await interaction.response.send_message(f'Hello, {interaction.user.mention}! 👋')
        logger.debug("Hello command completed successfully")

    @app_commands.command(name='serverinfo', description='Display server information')
    async def serverinfo_slash(self, interaction: discord.Interaction):
        '''Display server information'''
        logger = self.bot.logger.getChild('commands')
        logger.info(f'ServerInfo slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
        
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server!", ephemeral=True)
            return
            
        guild = interaction.guild
        embed = discord.Embed(
            title=f"📋 {guild.name} Server Info",
            color=0x7289da
        )
        
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        embed.add_field(name="🛡️ Verification", value=str(guild.verification_level).title(), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        logger.debug(f"Server info command: {guild.name} ({guild.member_count} members)")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='userinfo', description='Display information about a user')
    @app_commands.describe(user='The user to get information about (optional, defaults to you)')
    async def userinfo_slash(self, interaction: discord.Interaction, user: discord.Member = None):
        '''Display user information'''
        logger = self.bot.logger.getChild('commands')
        logger.info(f'UserInfo slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
        
        target_user = user or interaction.user
        
        embed = discord.Embed(
            title=f"👤 {target_user.display_name}",
            color=target_user.color if hasattr(target_user, 'color') else 0x99aab5
        )
        
        embed.add_field(name="🏷️ Username", value=str(target_user), inline=True)
        embed.add_field(name="🆔 ID", value=target_user.id, inline=True)
        embed.add_field(name="📅 Account Created", value=target_user.created_at.strftime("%B %d, %Y"), inline=True)
        
        if hasattr(target_user, 'joined_at') and target_user.joined_at:
            embed.add_field(name="📥 Joined Server", value=target_user.joined_at.strftime("%B %d, %Y"), inline=True)
        
        if hasattr(target_user, 'roles') and len(target_user.roles) > 1:
            roles = [role.mention for role in target_user.roles[1:]]  # Skip @everyone
            embed.add_field(name="🎭 Roles", value=" ".join(roles[:10]), inline=False)
        
        embed.set_thumbnail(url=target_user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='logtest', description='Demonstrate different log levels (admin only)')
    async def log_test_slash(self, interaction: discord.Interaction):
        '''Demonstrate different log levels with colored output'''
        logger = self.bot.logger.getChild('commands')
        logger.info(f'LogTest slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
        
        # Check if user has admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ This command requires administrator permissions.", 
                ephemeral=True
            )
            return

        logger.debug("🔍 DEBUG: This is a debug message")
        logger.info("ℹ️ INFO: This is an info message") 
        logger.warning("⚠️ WARNING: This is a warning message")
        logger.error("❌ ERROR: This is an error message")
        logger.critical("🚨 CRITICAL: This is a critical message")
        
        await interaction.response.send_message(
            "🎨 **Log Level Demo Complete!**\n"
            "Check your console/logs to see the different colored output levels:\n"
            "- 🔍 **DEBUG** (cyan)\n"
            "- ℹ️ **INFO** (green)\n" 
            "- ⚠️ **WARNING** (yellow)\n"
            "- ❌ **ERROR** (red)\n"
            "- 🚨 **CRITICAL** (bright red)",
            ephemeral=True
        )

    @app_commands.command(name='logs', description='Show recent bot logs (owner only)')
    @app_commands.describe(lines='Number of log lines to show (default: 10)')
    async def logs_slash(self, interaction: discord.Interaction, lines: int = 10):
        '''Show recent bot logs (owner only)'''
        logger = self.bot.logger.getChild('commands')
        logger.info(f'Logs slash command invoked by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')
        
        # Check if user is the bot owner
        app_info = await self.bot.application_info()
        if interaction.user.id != app_info.owner.id:
            logger.warning(f"Non-owner {interaction.user} tried to use logs command")
            await interaction.response.send_message("❌ This command is only available to the bot owner.", ephemeral=True)
            return
        
        lines = max(1, min(lines, 50))  # Limit between 1 and 50 lines
        
        try:
            with open('/app/data/logs/bot.log', 'r', encoding='utf-8') as f:
                log_lines = f.readlines()
                recent_logs = ''.join(log_lines[-lines:])
                
                if len(recent_logs) > 1900:  # Discord embed limit
                    recent_logs = recent_logs[-1900:]
                
                embed = discord.Embed(
                    title=f"📋 Recent Bot Logs ({lines} lines)",
                    description=f"```\n{recent_logs}```",
                    color=0x0099ff
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except FileNotFoundError:
            await interaction.response.send_message("❌ No log file found.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
            await interaction.response.send_message("❌ Error reading log file.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''Log when a member joins'''
        logger = self.bot.logger.getChild('events')
        logger.info(f"New member joined: {member} (ID: {member.id}) in {member.guild.name}")
        
        # Optional: Send a welcome message
        if member.guild.system_channel:
            embed = discord.Embed(
                title="👋 Welcome!",
                description=f"Welcome to {member.guild.name}, {member.mention}!",
                color=0x00ff00
            )
            try:
                await member.guild.system_channel.send(embed=embed)
            except discord.Forbidden:
                logger.debug("No permission to send welcome message")

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
        '''Handle slash command errors in this cog'''
        logger = self.bot.logger.getChild('commands')
        command_name = interaction.command.name if interaction.command else "unknown"
        
        if isinstance(error, app_commands.CommandOnCooldown):
            logger.debug(f'Slash command "{command_name}" on cooldown for {interaction.user}')
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"⏰ This command is on cooldown. Try again in {error.retry_after:.1f} seconds.",
                    ephemeral=True
                )
        else:
            logger.error(f'Error in slash command "{command_name}": {error}', exc_info=True)

async def setup(bot):
    await bot.add_cog(ExampleSlashCommands(bot))
    # Use the bot's logger instead of creating a new one
    logger = bot.logger.getChild('cogs')
    logger.info("ExampleSlashCommands cog loaded successfully")
"""
