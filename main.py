import asyncio
import os
import typing

import discord
from discord import app_commands
from dotenv import load_dotenv

from functions import *
from utilities import *


# TODO
# Add command for local `tree.sync` so that we don't get rate-limited during development
# Add auto-leave on program exit
# Detect channel change
# Implement whitelist


# UX variables
MESSAGE_TIMEOUT = 3

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
HOME_GUILD_ID = int(os.getenv('HOME_GUILD_ID'))
DEV_ID = int(os.getenv('DEV_ID'))

# Initialize bot
intents = discord.Intents().none()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

# Create client
client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)

# Get sync guild
sync_guild = discord.Object(id=HOME_GUILD_ID)


# Initialization behavior
@client.event
async def on_ready():
    print('Bot initializing, please wait...')
    print(
        'If launched quickly in succession, the bot will be rate-limited by discord. '
        'If you are not making any dev changes, you may uncomment `await tree.sync(...)` below to avoid this.')

    # Sync commands to home guild
    guild = client.get_guild(int(HOME_GUILD_ID))
    await tree.sync(guild=guild)
    print(f'Commands synced with {guild.name} ({guild.id})')

    # Status
    await client.change_presence(status=discord.Status.online, activity=discord.Game('🎵some tunes🎵'))

    # Setup
    client.queues = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print('Bot is configured, ready to operate.')


# Commands
@tree.command(name='sync', description='Synchronize commands globally', guild=discord.Object(id=HOME_GUILD_ID))
async def command_join(interaction):
    await interaction.response.defer(ephemeral=True)
    # Reject if not dev
    if interaction.user.id != DEV_ID:
        await interaction.followup.send('❌')
        return
    # Sync all commands
    loop = asyncio.get_running_loop()
    loop.create_task(tree.sync())
    await interaction.followup.send('👍')


@tree.command(name='join', description='Join the voice channel', guild=sync_guild)
async def command_join(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(join(client, interaction))
    await interaction.followup.send('👍')


@tree.command(name='leave', description='Leave the voice channel', guild=sync_guild)
async def command_leave(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(leave(client, interaction))


@tree.command(name='play', description='Play a song', guild=sync_guild)
async def command_play(interaction, url: str):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(play(client, interaction, url=url))


@tree.command(name='skip', description='Skip a song', guild=sync_guild)
async def command_skip(interaction, index: typing.Optional[int]):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(skip(client, interaction, index=index))


@tree.command(name='pause', description='Pause the current song', guild=sync_guild)
async def command_pause(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(pause(client, interaction))


@tree.command(name='resume', description='Resume the current song', guild=sync_guild)
async def command_resume(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(resume(client, interaction))


@tree.command(name='current', description='Show the currently playing song', guild=sync_guild)
async def command_playing(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewCurrent(client, interaction))


@tree.command(name='next', description='Show the next song', guild=sync_guild)
async def command_next(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewNext(client, interaction))


@tree.command(name='queue', description='Show the song queue', guild=sync_guild)
async def command_queue(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewQueue(client, interaction))


# Run
client.run(BOT_TOKEN)
