from asyncio import sleep
from contextlib import redirect_stdout
import io
import struct

import discord
import ffmpeg
import numpy as np
import pydub
from pytube import YouTube


# TODO
# Add crossfade between songs with pydub
# Add search feature for !play
# Add functionality for stream?
# Download while playing others
# Check which device works with InnerTube
# sort based on quality (already done?)
# Pass oauth message to end-user, rather than to server
# Only ask for OAuth if age restricted or unavailable
# Maybe call `after` after rather than recurse
# Refine `is_youtube_link`
# Store queueing user
# Fix clap at beginning and end of song
# Stream music rather than download all at once


### General utility
async def find_voice_client(client, reference, tries=1):
    for voice_client in client.voice_clients:
        if reference.guild == voice_client.guild:
            break

    else:
        # Retry (not used right now)
        if tries <= 1: return False
        await sleep(3)
        return await find_voice_client(client, reference, tries=tries-1)

    return voice_client


def get_queue(client, reference):
    # Make identifier
    # Right now, this is per-server queue
    hash = f'{reference.guild.id}'
    if not hash in client.queues:
        # Stored as (Queue, [Current URL])
        client.queues[hash] = ([], [None])
    return client.queues[hash]


def is_youtube_link(url):
    return 'youtube.com/' in url


def get_youtube_from_link(url):
    yt = YouTube(url)
    try:
        yt.check_availability()
        yt.bypass_age_gate()
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


### Behavior wrappers
async def type_during(reference, f):
    async with reference.channel.typing():
        await f


### Play functions
def play_next_queue(client, voice_client):
    if not get_queue(client, voice_client)[0]:
        get_queue(client, voice_client)[1][0] = None
        return
    play_url(voice_client, get_queue(client, voice_client)[0].pop(0), after=lambda err: play_next_queue(client, voice_client))


def play_url(voice_client, url, after=None):
    # Play if not YouTube
    if not is_youtube_link(url):
        # Can't FFmpegPCMAudio directly b/c youtube is blocked
        voice_client.play(discord.FFmpegPCMAudio(url))
        return

    # Find stream link
    # https://stackoverflow.com/a/67237301
    # Oauth needed for age-restricted, unlisted, or private videos
    yt = get_youtube_from_link(url)
    stream_url = yt.streams.filter(only_audio=True)[0].url
    source, _ = (
        ffmpeg
            .input(stream_url)
            .output('pipe:', format='s16le', acodec='pcm_s16le', ar=48000)
            .run(capture_stdout=True)
    )

    # Normalize with Pydub
    sound = pydub.AudioSegment(data=source, sample_width=2, frame_rate=48000, channels=2)
    sound = pydub.effects.normalize(sound, headroom=20)  # 6 is standard, but also very loud for most
    # sound.export("audio.wav", format="wav")  # DEBUG

    # Read as file
    audio = DumbReader(sound.raw_data)

    # Play
    voice_client.play(audio, after=after)
    get_queue(voice_client.client, voice_client)[1][0] = url


class DumbReader(discord.AudioSource):
    def __init__(self, source):
        self.index = 0
        self.source = source

    def read(self, window_size=3840):
        self.index += window_size
        return self.source[self.index : self.index + window_size]
