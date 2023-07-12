from utilities import *


### VC commands
async def join(client, interaction, verbose=True):
    # Get existing voice client and disconnect
    voice_client = await find_voice_client(client, interaction)
    if voice_client and voice_client.channel == interaction.user.voice.channel:
        if verbose:
            await interaction.followup.send('Already in channel.')
        return voice_client
    if voice_client:
        # Erase queue
        erase_queue(client, interaction)
        voice_client.cleanup()
        await voice_client.disconnect()

    # Get channel
    voice_channel = interaction.user.voice.channel
    # voice_channel = interaction.guild.voice_channels[0]  # DEBUG

    # Wait until connected
    voice_client = await voice_channel.connect(self_deaf=False)
    while not voice_client.is_connected():
        await asyncio.sleep(1)

    # Return
    if verbose:
        await interaction.followup.send('👍')
    return voice_client


async def leave(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.reply('Not in a voice channel.')
        return

    # Disconnect
    voice_client.cleanup()
    await voice_client.disconnect()

    await interaction.followup.send('👍')


### Play commands
async def play(client, interaction, *, url):
    # Get voice client and join user
    voice_client = await find_voice_client(client, interaction)
    if not voice_client or not voice_client.channel == interaction.user.voice.channel:
        voice_client = await join(client, interaction, verbose=False)

    # Defaults
    url = url if url else 'https://www.youtube.com/watch?v=y6120QOlsfU'

    # Add to queue
    queue = add_to_queue(client, interaction, url=url)
    if not queue:
        await interaction.followup.send('Queue is full. Please wait and try again')
        return

    # Play
    if not (queue['current'] or (len(queue['queue']) > 1)):
        await play_next_queue(client, voice_client)

    await interaction.followup.send('👍')


async def play_next_queue(client, voice_client):
    queue = cycle_queue(client, voice_client)
    if not queue['current']: return
    url, _ = queue['current'][0]
    loop = asyncio.get_running_loop()
    await play_url(voice_client, url, after=lambda err: loop.create_task(play_next_queue(client, voice_client)))


async def play_url(voice_client, url, after=None):
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
    download = (
        ffmpeg
            .input(stream_url)
            .output('pipe:', format='s16le', acodec='pcm_s16le', ar=48000, loglevel='error')
            .run_async(pipe_stdout=True)
    )
    data, _ = download.communicate()

    # Normalize with Pydub
    sound = pydub.AudioSegment(data=data, sample_width=2, frame_rate=48000, channels=2)
    sound = pydub.effects.normalize(sound, headroom=20)  # 6 is standard, but also very loud for most
    # sound.export('audio.wav', format='wav')  # DEBUG

    # Read as file/stream
    audio = RawReader(sound.raw_data)

    # Play
    voice_client.play(audio, after=after)


### Management commands
async def skip(client, interaction, *, index):
    # Defaults
    index = index if index else 0

    # Get queue
    queue = get_queue(client, interaction)

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send('No song is playing.')
        return
    if len(queue['queue']) < index:
        await interaction.followup.send(f'Queue only contains {len(queue["queue"])} songs.')
        return

    # Play next
    if index == 0:
        voice_client.stop()
    else:
        queue['queue'].pop(index - 1)  # Should this be added to history? Probably not

    await interaction.followup.send('👍')


async def pause(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not voice_client.is_playing():
        await interaction.followup.send('Not playing.')
        return

    # Pause
    voice_client.pause()

    await interaction.followup.send('👍')


async def resume(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not voice_client.is_paused():
        await interaction.followup.send('Not paused.')
        return

    # Resume
    voice_client.resume()

    await interaction.followup.send('👍')


### Preview commands
async def previewCurrent(client, interaction):
    queue = get_queue(client, interaction)

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not queue['current']:
        await interaction.followup.send('No song playing.')
        return

    # Show current
    url, user = queue['current'][0]
    await interaction.followup.send(f'Current Song: `{get_title_from_link(url)} ({user.name})`')


async def previewNext(client, interaction):
    queue = get_queue(client, interaction)

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not queue['queue']:
        await interaction.followup.send('Queue empty.')
        return

    # Show next
    url, user = queue['queue'][0]
    await interaction.followup.send(f'Next song: `{get_title_from_link(url)} ({user.name})`')


async def previewQueue(client, interaction):
    # Edge case where queue has something in it but queue doesn't will crash `previewQueue`
    # Get queue
    queue = get_queue(client, interaction)

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not queue['current']:
        await interaction.followup.send('Queue empty.')
        return

    # Show current
    url, user = queue['current'][0]
    reply = f'Now Playing: `{get_title_from_link(url)} ({user.name})`'

    # End early if no more songs
    if not queue['queue']:
        await interaction.followup.send(reply)
        return

    # Show queue
    reply += '\nSong Queue:'
    for i, (url, user) in enumerate(queue['queue']):
        reply += f'\n{i+1}. `{get_title_from_link(url)} ({user.name})`'
    await interaction.followup.send(reply)


async def previewHistory(client, interaction):
    # Get queue
    queue = get_queue(client, interaction)

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not queue['history']:
        await interaction.followup.send('History empty.')
        return

    # Show history
    reply = 'Song History:'
    for i, (url, user) in enumerate(queue['history']):
        reply += f'\n{i+1}. `{get_title_from_link(url)} ({user.name})`'
    await interaction.followup.send(reply)
