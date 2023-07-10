import asyncio
import os
import warnings

import discord
from dotenv import load_dotenv

from functions import *
from utilities import *


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

    # Status
    await client.change_presence(status=discord.Status.online, activity=discord.Game('🎵some tunes🎵'))

    # Setup
    client.queues = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop.run_forever()

    print('Bot is configured, ready to operate.')


# Commands
@client.event
async def on_message(message):
    # Parse
    command = message.content.split(' ')[0]
    if not command[0] == '!': return
    command = command[1:].lower()

    # Get loop
    loop = asyncio.get_running_loop()

    # Connect to voice channel
    if command == 'join':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, join(client, message)))

    # Disconnect
    elif command == 'leave':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, disconnect(client, message)))

    # Play music
    elif command == 'play':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, play(client, message)))

    # Skip current song
    elif command == 'skip':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, skip(client, message)))

    # Pause current song
    elif command == 'pause':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, pause(client, message)))

    # Resume current song
    elif command == 'resume':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, resume(client, message)))

    # Preview current song
    elif command == 'playing' or command == 'current':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, previewCurrent(client, message)))

    # Preview next song
    elif command == 'next':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, previewNext(client, message)))

    # Preview queue
    elif command == 'queue':
        await message.add_reaction('👍')
        loop.create_task(type_during(message, previewQueue(client, message)))

    else:
        await message.add_reaction('❌')

# Run
client.run(BOT_TOKEN)
