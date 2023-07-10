from utilities import *


# TODO
# MEDIUM PRIORITY Add time left in song/queue
# Handle edge case where play is called between songs?  Add lock?
# Maybe allow /play when user not in voice?
# Add auto disconnect after no activity period
# Add logic in `join` for user not in voice
# Add song swap functionality
# Add song history


async def join(client, interaction, verbose=True):
    # Get existing voice client and disconnect
    voice_client = await find_voice_client(client, interaction)
    if voice_client:
        # Erase queue
        get_queue(client, interaction)[0].clear()
        get_queue(client, interaction)[1][0] = None
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


async def play(client, interaction, *, url):
    # Defaults
    url = url if url else 'https://www.youtube.com/watch?v=y6120QOlsfU'  # 'https://www.youtube.com/watch?v=zvq9r6R6QAY'

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        voice_client = await join(client, interaction, verbose=False)

    # Add to queue
    queue = get_queue(client, interaction)
    queue[0].append(url)

    # Play
    if not (queue[1][0] or (len(queue[0]) > 1)):
        await play_next_queue(client, voice_client)

    await interaction.followup.send('👍')


async def skip(client, interaction, *, index):
    # Defaults
    index = index if index else 0

    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send('No song is playing.')
        return
    if len(get_queue(client, interaction)[0]) < index:
        await interaction.followup.send(f'Queue only contains {len(get_queue(client, interaction)[0])} songs.')
        return

    # Play next
    if index == 0:
        voice_client.stop()
    else:
        get_queue(client, interaction)[0].pop(index - 1)

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


async def previewCurrent(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not get_queue(client, interaction)[1][0]:
        await interaction.followup.send('No song playing.')
        return

    # Show current
    url = get_queue(client, interaction)[1][0]
    await interaction.followup.send(f'Current Song: `{get_title_from_link(url)} ({url})`')


async def previewNext(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not get_queue(client, interaction)[0]:
        await interaction.followup.send('Queue empty.')
        return

    # Show next
    url = get_queue(client, interaction)[0][0]
    await interaction.followup.send(f'Next song: `{get_title_from_link(url)} ({url})`')


async def previewQueue(client, interaction):
    # Get voice client
    voice_client = await find_voice_client(client, interaction)
    if not voice_client:
        await interaction.followup.send('Not in a voice channel.')
        return
    if not get_queue(client, interaction)[1][0]:
        await interaction.followup.send('Queue empty.')
        return

    # Play next
    url = get_queue(client, interaction)[1][0]
    reply = f'Now Playing: `{get_title_from_link(url)} ({url})`'
    for i, url in enumerate(get_queue(client, interaction)[0]):
        reply += f'\n{i+1}. `{get_title_from_link(url)} ({url})`'
    await interaction.followup.send(reply)
