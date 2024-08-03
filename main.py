import discord
from discord.ext import commands

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Read the configuration file
config = read_config("config.txt")

# Retrieve the token and channel ID from the configuration file
TOKEN = config['TOKEN']
CHANNEL_ID = int(config['CHANNEL_ID'])

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to track consecutive messages
user_message_count = {}

global counter
counter = 160
global last_message


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
 
    messages = [msg async for msg in channel.history(limit=2)]
    if messages:
        last_message = messages[0]
        global counter
        try:
            counter = int(last_message.content) + 1
        except ValueError:
            print("The last message is not a number")
    

@bot.event
async def on_message(message):
    global counter
    
    channel = bot.get_channel(CHANNEL_ID)
 
    messages = [msg async for msg in channel.history(limit=2)]
    last_message = messages[0]  
    second_last_message = messages[1]  

    if not message.content.isdigit(): # delete if the message is a string
        await message.delete()
        print(f"Message deleted: '{message.content}' (does not contain only numbers)")
        return
    
    if int(message.content) == counter:
        counter += 1
        print(f"The counter is at {counter}")
    
    else:
        await message.delete()
        print(f"Last message deleted because {message} !== {counter}")

    if last_message.author == second_last_message.author:
        if message.content.isdigit():
            await last_message.delete()
            print("The last message was deleted because last_message.author == second_last_message.author")
            counter -= 1
              
# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run(TOKEN)

