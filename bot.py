import discord
from discord.ext import commands
import random
import string
import time
import os
from dotenv import load_dotenv
from geo_guesser import geo_guesser_attack

load_dotenv('.env')
# Replace with your bot's token
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
TOKEN = os.getenv("TOKEN")

# Intents (not needed for this basic command)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Create the slash command
@bot.command(name='geoguess')
async def geoguess(ctx, target_username: str):
    await ctx.send(f"Starting the GeoGuesser attack on {target_username}...")

    # Trigger the GeoGuesser attack logic
    result = geo_guesser_attack(target_username)

    # Send the result back
    await ctx.send(f"GeoGuess result for {target_username}: {result}")

# Run the bot with your token from Discord Developer Portal
bot.run(TOKEN)