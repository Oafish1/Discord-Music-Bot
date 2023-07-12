import asyncio
import struct
import warnings

import discord
import ffmpeg
import pydub
from pytube import YouTube


# Config
with open('.config', 'r') as f:
    exec(f.read())


### General utility
async def find_voice_client(client, interaction, tries=1):
    for voice_client in client.voice_clients:
        if interaction.guild == voice_client.guild:
            break

    else:
        # Retry (not used right now)
        if tries <= 1: return False
        await asyncio.sleep(3)
        return await find_voice_client(client, interaction, tries=tries-1)

    # Safeguard for spam joins
    while not voice_client.is_connected():
        print('Sleeping FVC. Normally a result of a `play` command before the `join` command finishes.  If this persists, please make a bug report.')
        await asyncio.sleep(1)

    return voice_client


def get_queue_hash(interaction):
    return f'{interaction.guild.id}'


def erase_queue(client, interaction):
    hash = get_queue_hash(interaction)
    if hash in client.queues:
        client.queues.pop(hash)


def get_queue(client, interaction):
    # Make identifier
    # Right now, this is per-server queue
    hash = get_queue_hash(interaction)
    if not hash in client.queues:
        # Stored as (Queue, [Current URL])
        client.queues[hash] = {
            'current': [],
            'queue': [],
            'history': [],
        }
    return client.queues[hash]


def add_to_queue(client, interaction, *, url):
    # Get queue
    queue = get_queue(client, interaction)
    # Check if full
    if len(queue['queue']) >= MAX_QUEUE:
        return False
    # Add to queue
    queue['queue'].append((url, interaction.user))  # Could add lockfile but that's overkill

    return queue


def cycle_queue(client, interaction):
    # Get queue
    queue = get_queue(client, interaction)
    # Move current to history
    if queue['current']:
        queue['history'].insert(0,  queue['current'].pop(0))
        if len(queue['history']) > MAX_QUEUE_HISTORY:
            queue['history'].pop(-1)
    # Pop from queue to current
    if queue['queue']:
        queue['current'].append(queue['queue'].pop(0))
        if len(queue['current']) > 1:  # Could just overwrite, but where's the fun in that?  This way we know if there's a race condition
            warnings.warn(f'Current now has length {len(queue["current"])} when it should be <=1.')

    return queue


def is_youtube_link(url):
    return 'youtube.com/' in url


def get_youtube_from_link(url):
    yt = YouTube(url)
    try:
        yt.check_availability()
        yt.bypass_age_gate()
        yt.streams
    except:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        # Not sure if it's possible to pipe to user, since input() command freezes
        # f = io.StringIO()
        # with redirect_stdout(f):
        #     yt.streams
        # s = f.getvalue()
        # print(s)
    return yt


def get_title_from_link(url):
    # Only works for YouTube
    if not is_youtube_link(url): return url
    return YouTube(url).title


### Classes
class RawReader(discord.AudioSource):
    def __init__(self, data, sampling_rate=48_000, channels=2, frame_length=20):
        self.index = 0
        self.data = data

        self.sampling_rate = sampling_rate
        self.channels = channels
        self.frame_length = frame_length  # ms

        # Calculate frame size
        self.samples_per_frame = int(self.sampling_rate * self.frame_length / 1000)
        self.sample_size = struct.calcsize('h') * self.channels
        self.frame_size = self.samples_per_frame * self.sample_size

    def read(self):
        # Increment
        self.index += self.frame_size
        # Return if not enough data
        if self.index + self.frame_size > len(self.data):
            # Clip to avoid clapping noise
            return b''
        # Return data
        return self.data[self.index : self.index + self.frame_size]

    def is_opus(self):
        return False

    def cleanup(self):
        pass
