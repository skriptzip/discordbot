import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}', flush=True)

@bot.command()
async def ping(ctx):
    print(f'Ping command invoked by {ctx.author}', flush=True)
    await ctx.send('Pong!')

if __name__ == '__main__':
    bot.run(TOKEN)
