# Discord Music Bot

Barebones music bot for discord that works with YouTube.

## Functions

`!join`: Join the voice channel\
`!leave`: Leave the voice channel\
`!play <link>`: Play the music specified at `<link>`\
`!skip`: Skip the currently playing song\
`!pause`: Pause the current song\
`!resume`: Resume the current song\
`!playing !current`: Show the currently playing song\
`!next`: Show the next song\
`!queue`: Display all songs in the queue

## Installation

### Cloning the Repository

Clone the repository

```bash
git clone https://github.com/Oafish1/Discord-Music-Bot
cd Discord-Music-Bot-main
```

### Bot Configuration

Create a discord bot account and get a token. This process is seen [here](https://discordgsm.com/guide/how-to-get-a-discord-bot-token).  Configure the `Bot` and `OAuth2` tabs as below.  After configuring, invite the bot to your server using the link generator on the `OAuth2` dropdown (select bot and permissions as below).

<img src='img\privileged_gateway_intents.PNG' alt='Privileged Gateway Intents' width='600'/>
<img src='img\default_authorization_link.PNG' alt='Default Authorization Link' width='600'/>

Create a file `.env` with the following contents in the home directory, where `<bot-token>` is your token.

```text
BOT_TOKEN = '<bot-token>'
```

### Install Dependencies

Also download [FFMPEG](https://ffmpeg.org/download.html) and add `ffmpeg/bin` to your `PATH` environment variable.

Install dependencies

```bash
pip install -r requirements.txt
```

*You may need to install `pytube` for `python` separately.  As of `2023-07-09`, the current distribution of `pytube` isn't able to parse links properly, and a modification needs to be made to `cipher.py` in accordance with [this issue](https://github.com/pytube/pytube/issues/1678#issuecomment-1603948730).*

### Run the Bot

Start the script

```bash
python main.py
```

On the first run, the program will ask for `OAuth` information, and will have you configure the program with google by entering a device code online.  Make sure you authorize with the base channel for any email chosen.  This is so that age-restricted videos may be played.

**If you don't care about this feature or don't wish to log in, change `use_oauth=True` to `False` in `utilities.py`.**

For quick access, you can also create a batch script

```bash
@echo off
cd <path-to-repository>
python main.py
```

Enjoy!
