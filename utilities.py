from asyncio import sleep
import struct

import discord
import ffmpeg
import pydub
from pytube import YouTube


# TODO
# HIGH PRIORITY Cut out clap at beginning and end of song
# HIGH PRIORITY Add song history
# HIGH PRIORITY Cut playlist tag from YouTube URL
# HIGH PRIORITY Remove FFMPEG printing, add debug prints for HOME_GUILD
# Store creds for each guild?
# Add message for skipping song/reject if bad link instead of adding to queue
# Maybe skip to song in queue option?  Maybe reorder?
# Replace song function?
# Cleaner solution for `PCMAudio`
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
# Stream music rather than download all at once


### General utility
async def find_voice_client(client, interaction, tries=1):
    for voice_client in client.voice_clients:
        if interaction.guild == voice_client.guild:
            break

    else:
        # Retry (not used right now)
        if tries <= 1: return False
        await sleep(3)
        return await find_voice_client(client, interaction, tries=tries-1)

    return voice_client


def get_queue(client, interaction):
    # Make identifier
    # Right now, this is per-server queue
    hash = f'{interaction.guild.id}'
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


### Behavior wrappers
# async def type_during(reference, f):
#     async with reference.channel.typing():
#         await f


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
    # Nested for compatibility
    audio = discord.PCMAudio(RawReader(sound.raw_data))

    # Play
    voice_client.play(audio, after=after)
    get_queue(voice_client.client, voice_client)[1][0] = url


### Classes
class RawReader(discord.AudioSource):
    def __init__(self, source):
        self.index = 0
        self.source = source
        self.frame_size = int(48000 / 1000 * 20) * struct.calcsize('h') * 2

    def read(self):
        self.index += self.frame_size
        return self.source[self.index : self.index + self.frame_size]

    def is_opus(self):
        return False

    def cleanup(self):
        pass
