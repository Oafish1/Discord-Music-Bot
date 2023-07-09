from asyncio import sleep
from contextlib import redirect_stdout
import io
import struct

import discord
import ffmpeg
import numpy as np
from pytube import YouTube


# TODO
# Add functionality for stream?
# Download while playing others
# Check which device works with InnerTube
# Maybe just save to s16le?
# sort based on quality (already done?)
# Pass oauth message to end-user, rather than to server
# Only ask for OAuth if age restricted or unavailable
# Maybe call `after` after rather than recurse
# Refine `is_youtube_link`
# Store queueing user


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
            .output('pipe:', format='wav', acodec='pcm_s16le', ar=48000)
            .run(capture_stdout=True)
    )

    # Remove metadata header
    data_start_index = source.find(b'data') + 8
    header, source = source[:data_start_index], source[data_start_index:]

    # Read short little endian
    source = np.array(struct.unpack(f'<{"h" * (len(source) // 2)}', source))

    # Normalize
    max_peak = 2**11 - 1  # 2**15 - 1 makes the song max volume
    source = source / (np.max(np.abs(source)) / max_peak)
    source = source.astype(np.int16)

    # Write short little endian
    source = struct.pack(f'<{"h" * (len(source))}', *source)

    # Play
    # Download locally (dumb, not multi-instance safe)
    # with open('audio.wav', 'wb') as f:
    #     f.write(header + source)
    # audio = discord.FFmpegPCMAudio('audio.wav')

    # Read var as file (even dumber, but multi-instance safe)
    # audio = discord.PCMAudio(DumbReader(source))

    # Read whole file (okayer)
    audio = DumbReader(source)

    # Read filestream (like a competent person)
    # TODO

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
