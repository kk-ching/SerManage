import discord
from discord.ext import commands
from WakeUp import *
import socket
import os
from dotenv import load_dotenv
import time


def timestamped_print(*args, **kwargs):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, **kwargs)

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
    timestamped_print(f"Received command to start the server from {ctx.author}.")
    if is_reachable(ip_address):
        await ctx.send("Server is already running desuwa")
        return
    await ctx.send("Starting the server... Please wait.")
    if wake_up_server(mac_address, ip_address, subnet_broadcast):
        await ctx.send("Server is now up and running!")
    else:
        await ctx.send("Failed to wake up the server after multiple attempts.")

def is_internet_available(target = "discord.com"):
    try:
        socket.create_connection((target, 80), timeout=5)
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    timestamped_print("Startup Script triggered at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    count = 0
    while not is_internet_available():
        count += 1
        timestamped_print(f"Internet not available, retrying in 10 seconds... (count: {count})")
        time.sleep(10)
    
    timestamped_print("Access to the internet is available. Starting the bot...")
    bot.run(token)
