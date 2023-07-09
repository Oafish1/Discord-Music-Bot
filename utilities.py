from asyncio import sleep

import discord
import ffmpeg
from pytube import YouTube


### General utility
async def find_voice_client(client, reference, tries=5):
    if not tries: return False

    for voice_client in client.voice_clients:
        if reference.guild == voice_client.guild:
            break

    else:
        # Retry
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


### Play functions
def play_next_queue(client, voice_client):
    if not get_queue(client, voice_client)[0]: return
    play_url(voice_client, get_queue(client, voice_client)[0].pop(0), after=lambda: play_next_queue(client, voice_client))


def play_url(voice_client, url, after=None):
    # Play if not YouTube
    if not url.startswith('https://www.youtube.com/'):
        # Can't FFmpegPCMAudio directly b/c youtube is blocked
        voice_client.play(discord.FFmpegPCMAudio(url))
        return

    # Find stream link
    # https://stackoverflow.com/a/67237301
    # TODO: Download while playing others
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)  # , use_oauth=True, allow_oauth_cache=True
    stream_url = yt.streams.filter(only_audio=True)[0].url  # TODO sort based on quality
    print(ffmpeg.input(stream_url).output('pipe:', format='wav', acodec='pcm_s16le').audio)
    source, _ = (
        ffmpeg
            .input(stream_url)
            .output('pipe:', format='wav', acodec='pcm_s16le', ar=48000)
            .run(capture_stdout=True)
    )

    # Play
    # Download locally (dumb, not multi-instance safe)
    # with open('audio.wav', 'wb') as f:
    #     f.write(source)
    # audio = discord.FFmpegPCMAudio('audio.wav')

    # Read var as file (even dumber, but multi-instance safe)
    # audio = discord.PCMAudio(DumbReader(source))

    # Read whole file (okayer)
    audio = DumbReader(source)

    # Read filestream (like a competent person)
    # TODO

    # Play
    # TODO: Normalize volume
    voice_client.play(audio, after=lambda err: after())
    get_queue(voice_client.client, voice_client)[1][0] = url


class DumbReader(discord.AudioSource):
    def __init__(self, source):
        self.index = 0
        self.source = source

    def read(self, window_size=3840):
        self.index += window_size
        return self.source[self.index : self.index + window_size]
