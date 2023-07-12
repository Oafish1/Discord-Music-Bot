import asyncio
import os
import typing

import discord
from discord import app_commands
from dotenv import load_dotenv
import numpy as np

from functions import *
from utilities import *


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
client = discord.Client(intents=intents, status=discord.Status.online, activity=discord.Game('🎵some tunes🎵'))
tree = app_commands.CommandTree(client)


# Initialization behavior
@client.event
async def on_ready():
    print('Bot initializing, please wait...')

    # Global sync
    await tree.sync()

    # Setup
    client.queues = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print('Bot is configured, ready to operate.')


# Commands
@tree.command(name='sync_global', description='Synchronize commands globally', guild=discord.Object(id=HOME_GUILD_ID))
async def command_sync_global(interaction):
    await interaction.response.defer(ephemeral=True)
    # Reject if not dev
    # owner = interaction.user == interaction.guild.owner
    # admin = np.array([role.permissions.administrator for role in interaction.user.roles]).any()
    dev = interaction.user.id == DEV_ID
    if not (dev):
        await interaction.followup.send('❌')
        return
    # Sync all commands globally
    await tree.sync()
    print(f'Commands globally synced')
    await interaction.followup.send('👍')


@tree.command(name='sync_local', description='Synchronize commands locally')
async def command_sync_local(interaction):
    await interaction.response.defer(ephemeral=True)
    # Reject if not dev, owner, or admin
    owner = interaction.user == interaction.guild.owner
    admin = np.array([role.permissions.administrator for role in interaction.user.roles]).any()
    dev = interaction.user.id == DEV_ID
    if not (dev or owner or admin):
        await interaction.followup.send('❌')
        return
    # Sync all commands locally
    await tree.sync(guild=interaction.guild)
    print(f'Commands synced with {interaction.guild.name} ({interaction.guild.id})')
    await interaction.followup.send('👍')


@tree.command(name='join', description='Join the voice channel')
async def command_join(interaction):
    await interaction.response.defer(ephemeral=True)
    await join(client, interaction)


@tree.command(name='leave', description='Leave the voice channel')
async def command_leave(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(leave(client, interaction))


@tree.command(name='play', description='Play a song')
async def command_play(interaction, url: str):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(play(client, interaction, url=url))


@tree.command(name='skip', description='Skip a song')
async def command_skip(interaction, index: typing.Optional[int]):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(skip(client, interaction, index=index))


@tree.command(name='pause', description='Pause the current song')
async def command_pause(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(pause(client, interaction))


@tree.command(name='resume', description='Resume the current song')
async def command_resume(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(resume(client, interaction))


@tree.command(name='current', description='Show the currently playing song')
async def command_current(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewCurrent(client, interaction))


@tree.command(name='next', description='Show the next song')
async def command_next(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewNext(client, interaction))


@tree.command(name='queue', description='Show the song queue')
async def command_queue(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewQueue(client, interaction))


@tree.command(name='history', description='Show the previously played songs')
async def command_history(interaction):
    await interaction.response.defer(ephemeral=True)
    loop = asyncio.get_running_loop()
    loop.create_task(previewHistory(client, interaction))


# Run
client.run(BOT_TOKEN)
