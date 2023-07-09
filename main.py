import os
import warnings

import discord
from dotenv import load_dotenv

from functions import *


# Load environment
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
HOME_GUILD = os.getenv('HOME_GUILD')

# TODO: Implement whitelist

# Initialize bot
intents = discord.Intents().none()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

client = discord.Client(command_prefix='!', intents=intents)


# Initialization behavior
# TODO: Add auto-leave on exit
@client.event
async def on_ready():
    # Check for home guild (verbose output)
    # for guild in client.guilds:
    #     if int(guild.id) == int(HOME_GUILD):
    #         print('Bot connected to debug server.')
    #         break
    # else:
    #     warnings.warn('Bot not connected to verbose server.')

    # Setup
    client.queues = {}
    print('Bot is configured, ready to operate.')


# Commands
@client.event
async def on_message(message):
    # Parse
    command = message.content.split(' ')[0]
    if not command[0] == '!': return
    command = command[1:]

    # Connect to voice channel
    if command == 'join':
        await join(client, message)

    # Disconnect
    elif command == 'leave':
        await disconnect(client, message)

    # Play music
    elif command == 'play':
        await play(client, message)

    # Skip current song
    elif command == 'skip':
        await skip(client, message)

    # Pause current song
    elif command == 'pause':
        await pause(client, message)

    # Resume current song
    elif command == 'resume':
        await resume(client, message)

    # Preview current song
    elif command == 'playing' or command == 'current':
        await previewCurrent(client, message)

    # Preview next song
    elif command == 'next':
        await previewNext(client, message)

    # Preview queue
    elif command == 'queue':
        await previewQueue(client, message)

# Run
client.run(BOT_TOKEN)
