import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from huggingface import get_model_response
import utils

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="", intents=intents)
system_prompt = ""
admin_list = []  # list of admin ids in integers

async def set_dnd_status():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.CustomActivity(name="beep boop")
    )

async def fetch_specific_message(env_message_path: str) -> str:
    channel_id, message_id = os.getenv(env_message_path).split(":")  # <channel_id>:<message_id>
    channel = bot.get_channel(int(channel_id))
    message = await channel.fetch_message(message_id)
    return message.content

async def set_admin_list():
    global admin_list
    message_content = await fetch_specific_message("ADMIN_LIST_PATH")
    admin_list = list(map(int, message_content.split(";")))

async def set_system_prompt():
    global system_prompt
    system_prompt = await fetch_specific_message("SYSTEM_PROMPT_PATH")

async def handle_stats(message):
    version = utils.get_git_tag()
    uptime = utils.get_uptime()
    content = f">>> **version**: {version}\n**uptime**: {uptime}"
    await message.channel.send(content)

async def handle_reload(message):
    await set_admin_list()
    await set_system_prompt()
    await message.channel.send("reloaded admin list and system prompt")

@bot.event
async def on_ready():
    print(f"{bot.user} online")
    await set_dnd_status()
    await set_admin_list()
    await set_system_prompt()

@bot.event
async def on_message(message):
    if (message.author.bot or 
        bot.user not in message.mentions or  # ignore if the bot is not mentioned
        not message.content.strip() or # ignore empty messages
        isinstance(message.channel, discord.DMChannel)): # ignore dms
        return

    user_message = message.content.replace(f"<@!{bot.user.id}>", "").strip()
    reply_to_message = message.reference

    if not user_message:
        return

    if "--" in user_message:
        if message.author.id in admin_list:
            if "--ss" in user_message:
                await handle_stats(message)
                return
            elif "--rl" in user_message:
                await handle_reload(message)
                return

    try:
        async with message.channel.typing():
            response = get_model_response(system_prompt, user_message)
    except Exception as e:
        response = "something went wrong with me..."
        raise Exception(e)

    if reply_to_message:
        await message.channel.send(response, reference=message)
    else:
        await message.channel.send(response)
