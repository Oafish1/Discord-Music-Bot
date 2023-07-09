# Discord Music Bot

Barebones music bot for discord that works with YouTube.

## Functions

`!join`: Join the voice channel\
`!leave`: Leave the voice channel\
`!play <link>`: Play the music specified at <link>\
`!skip`: Skip the currently playing song\
`!pause`: Pause the current song\
`!resume`: Resume the current song\
`!playing !current`: Show the currently playing song\
`!next`: Show the next song\
`!queue`: Display all songs in the queue

## Installation

Clone the repository,
```bash
git clone https://github.com/Oafish1/Discord-Music-Bot
cd Discord-Music-Bot
```

Create a discord bot account and get a token. This process is seen [here](https://discordgsm.com/guide/how-to-get-a-discord-bot-token).  Configure the `Bot` and `OAuth2` tabs as below.  After configuring, invite the bot to your server using the link on the OAuth2 page.

<img src='img\privileged_gateway_intents.PNG' alt='Privileged Gateway Intents' width='600'/>
<img src='img\default_authorization_link.PNG' alt='Default Authorization Link' width='600'/>

Create a text file `.env` with the following contents in the home directory, where `<bot token>` is your token.
```text
BOT_TOKEN = <bot token>
```

Install dependencies,
```bash
pip install -r requirements.txt
```

Run the bot,
```bash
python main.py
```

Congratulations!
