import os
from discordbot import bot
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
bot.run(DISCORD_TOKEN)
