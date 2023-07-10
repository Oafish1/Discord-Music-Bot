from utilities import *


# TODO
# HIGH PRIORITY Add remove from queue function
# Add auto disconnect after no activity period
# Add logic in `join` for user not in voice


async def join(client, message):
    # Get existing voice client and disconnect
    voice_client = await find_voice_client(client, message)
    if voice_client:
        # Erase queue
        get_queue(client, message)[0].clear()
        get_queue(client, message)[1][0] = None
        voice_client.cleanup()
        await voice_client.disconnect()

    voice_channel = message.author.voice.channel
    # voice_channel = message.guild.voice_channels[0]  # DEBUG
    voice_client = voice_channel.connect(self_deaf=False)

    return await voice_client


async def disconnect(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return

    # Disconnect
    voice_client.cleanup()
    await voice_client.disconnect()


async def play(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        voice_client = await join(client, message)

    # Extract url
    DEFAULT_LINK = 'https://www.youtube.com/watch?v=zvq9r6R6QAY'
    url = message.content.split(' ')[1] if len(message.content.split(' ')) > 1 else DEFAULT_LINK

    # Add to queue
    get_queue(client, message)[0].append(url)

    # Play
    if not voice_client.is_playing():
        play_next_queue(client, voice_client)


async def skip(client, message):
    split_message = message.content.split(' ')
    index = int(split_message[1]) if len(split_message) > 1 else 0

    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not voice_client.is_playing() or voice_client.is_paused():
        await message.reply('No song is playing.')
        return
    if len(get_queue(client, message)[0]) < index:
        await message.reply(f'Queue only contains {len(get_queue(client, message)[0])} songs.')
        return

    # Play next
    if index == 0:
        voice_client.stop()
        return
    get_queue(client, message)[0].pop(index - 1)


async def pause(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not voice_client.is_playing():
        await message.reply('Not playing.')
        return

    # Pause
    voice_client.pause()


async def resume(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not voice_client.is_paused():
        await message.reply('Not paused.')
        return

    # Resume
    voice_client.resume()


async def previewCurrent(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[1][0]:
        await message.reply('No song playing.')
        return

    # Show current
    url = get_queue(client, message)[1][0]
    await message.reply(f'Current Song: `{get_title_from_link(url)} ({url})`')


async def previewNext(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[0]:
        await message.reply('Queue empty.')
        return

    # Show next
    url = get_queue(client, message)[0][0]
    await message.reply(f'Next song: `{get_title_from_link(url)} ({url})`')


async def previewQueue(client, message):
    # Get voice client
    voice_client = await find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[1]:
        await message.reply('Queue empty.')
        return

    # Play next
    url = get_queue(client, message)[1][0]
    reply = f'Now Playing: `{get_title_from_link(url)} ({url})`'
    for i, url in enumerate(get_queue(client, message)[0]):
        reply += f'\n{i+1}. `{get_title_from_link(url)} ({url})`'
    await message.reply(reply)
