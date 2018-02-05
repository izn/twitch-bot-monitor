# twitch-bot-monitor

Simple Twitch bot that stores the ocurrencies of words used in a Twitch channel with a web interface.

# Getting Started

Install directly from the GitHub repository


    git clone git@github.com:izn/twitch-bot-monitor.git
    cd twitch-bot-monitor
    pip install -r requirements/package.txt


## Configuration

Start copying the ``env.example`` to ``.env``

    cp env.example .env

Then fill the environment variables on ``.env`` file.

``TWITCH_LOGIN``: Your Twitch username

``TWITCH_OAUTH``: Twitch OAuth ([Generate here](https://twitchapps.com/tmi/))

``TWITCH_CHANNEL``: The channel the bot will monitor (e.g.: ``dotastarladder_en``)

## Usage

To start monitoring, use

    python twitchbot/bot.py

To run the web server interface, use

    python twitchbot/server.py

Access the web interface: http://127.0.0.1:5000/

## Tests

Just `tox`
