import os
import warnings

import discord
from dotenv import load_dotenv

from functions import *


# TODO
# Add auto-leave on program exit
# Detect channel change
# Implement whitelist


# Load environment
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
HOME_GUILD = os.getenv('HOME_GUILD')

# Initialize bot
intents = discord.Intents().none()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

client = discord.Client(command_prefix='!', intents=intents)


# Initialization behavior
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
    command = command[1:].lower()

    # Connect to voice channel
    if command == 'join':
        await message.add_reaction('👍')
        await join(client, message)

    # Disconnect
    elif command == 'leave':
        await message.add_reaction('👍')
        await disconnect(client, message)

    # Play music
    elif command == 'play':
        await message.add_reaction('👍')
        await play(client, message)

    # Skip current song
    elif command == 'skip':
        await message.add_reaction('👍')
        await skip(client, message)

    # Pause current song
    elif command == 'pause':
        await message.add_reaction('👍')
        await pause(client, message)

    # Resume current song
    elif command == 'resume':
        await message.add_reaction('👍')
        await resume(client, message)

    # Preview current song
    elif command == 'playing' or command == 'current':
        await message.add_reaction('👍')
        await previewCurrent(client, message)

    # Preview next song
    elif command == 'next':
        await message.add_reaction('👍')
        await previewNext(client, message)

    # Preview queue
    elif command == 'queue':
        await message.add_reaction('👍')
        await previewQueue(client, message)

    else:
        await message.add_reaction('❌')

# Run
client.run(BOT_TOKEN)
