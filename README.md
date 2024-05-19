
# IKEA Offers Discord Bot

This project consists of a Python-based bot that fetches offers from the IKEA circular API and posts new entries to a specified Discord channel. The project includes two main components: a script for fetching and storing offers (`request.py`) and a Discord bot (`bot.py`) that posts updates to a Discord channel.

## Features

- Fetches offers from the IKEA circular API.
- Stores offers in an SQLite database.
- Notifies a Discord bot about new entries.
- Posts new offers to a specified Discord channel with detailed information.

## Prerequisites

- Python 3.x
- `requests` library
- `sqlite3` library (comes with Python)
- `discord.py` library
- `Flask` library

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/ikea-offers-bot.git
   cd ikea-offers-bot
   ```

2. **Install dependencies**:
   ```sh
   pip install requests discord.py Flask
   ```

3. **Set up Discord bot**:
   - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token and save it in a file named `token.txt` in the project directory.
   - Replace `CHANNEL_ID` in `bot.py` with the ID of the Discord channel where you want the bot to post updates.

## Usage

1. **Start the bot**:
   ```sh
   python bot.py
   ```

2. **Fetching and storing offers**:
   - The `request.py` script is run periodically by the bot to fetch offers from the IKEA circular API.
   - New offers are stored in an SQLite database (`ikea_offers.db`).
   - The bot posts new entries to the specified Discord channel.


## Configuration

- **API URL**: Defined in `request.py`.
- **Database**: SQLite database (`ikea_offers.db`) is created and used to store offers.
- **Discord Channel**: Replace `CHANNEL_ID` in `bot.py` with the ID of your Discord channel.

## Endpoints

- `/notify`: Endpoint in `bot.py` that receives notifications about new offers from `request.py`.

