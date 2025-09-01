# Example: How to add new commands to your bot
# 
# This file shows how to create a cog (command group) that can be loaded into the main bot.
# To use this example:
# 1. Uncomment the code below
# 2. In bot.py, add: await bot.load_extension('example_commands')
# 3. Restart the container

"""
import discord
from discord.ext import commands

class ExampleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}!')

    @commands.command(name='info')
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info",
            description="This is an example Discord bot!",
            color=0x00ff00
        )
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ExampleCommands(bot))
"""
