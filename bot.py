import discord
from discord.ext import commands
from WakeUp import *
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

mac_address = os.getenv("mac_address")
ip_address = os.getenv("ip_address")
subnet_broadcast = os.getenv("subnet_broadcast")

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN environment variable is not set.")

if not mac_address or not ip_address or not subnet_broadcast:
    raise ValueError("One or more server configuration environment variables are not set.")

@bot.command()
async def start(ctx):
    if is_reachable(ip_address):
        await ctx.send("Server is already running desuwa")
        return
    await ctx.send("Starting the server... Please wait.")
    if wake_up_server(mac_address, ip_address, subnet_broadcast):
        await ctx.send("Server is now up and running!")
    else:
        await ctx.send("Failed to wake up the server after multiple attempts.")




bot.run(token)
