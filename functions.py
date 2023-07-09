from utilities import *


async def join(client, message):
    # Get existing voice client and disconnect
    # TODO: Add logic for user not in voice
    voice_client = find_voice_client(client, message)
    if voice_client:
        voice_client.cleanup()
        await voice_client.disconnect()

    voice_channel = message.author.voice.channel
    voice_client = voice_channel.connect(self_deaf=False)

    return await voice_client


async def disconnect(client, message):
    # Get voice client
    voice_client = find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return

    # Disconnect
    voice_client.cleanup()
    await voice_client.disconnect()


async def play(client, message):
    # Get voice client
    voice_client = find_voice_client(client, message)
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
    # Get voice client
    voice_client = find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not voice_client.is_playing() or voice_client.is_paused():
        await message.reply('Queue is empty.')
        return

    # Play next
    voice_client.stop()


async def pause(client, message):
    # Get voice client
    voice_client = find_voice_client(client, message)
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
    voice_client = find_voice_client(client, message)
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
    voice_client = find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[1][0]:
        await message.reply('No song playing.')
        return

    # Show current
    await message.reply(f'Current Song: {get_queue(client, message)[1][0]}')


async def previewNext(client, message):
    # Get voice client
    voice_client = find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[0]:
        await message.reply('Queue empty.')
        return

    # Show next
    await message.reply(f'Next song: {get_queue(client, message)[0][0]}')


async def previewQueue(client, message):
    # Get voice client
    voice_client = find_voice_client(client, message)
    if not voice_client:
        await message.reply('Not in a voice channel.')
        return
    if not get_queue(client, message)[0]:
        await message.reply('Queue empty.')
        return

    # Play next
    await message.reply(
        'Current Queue:\n'
        + '\n'.join(get_queue(client, message)[0])
    )
