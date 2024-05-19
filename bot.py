import discord
from discord.ext import commands
from flask import Flask, request
import threading
import signal
import sys
import asyncio

# Replace 'YOUR_BOT_TOKEN' with your bot's token
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Replace 'YOUR_CHANNEL_ID' with the ID of the channel you want to send messages to
CHANNEL_ID = 1241676803106668646

# Intents are necessary to allow the bot to access certain events
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
app = Flask(__name__)
app.config['ENV'] = 'production'

@bot.command()
async def send(ctx, *, message: str):
    """Sends a message to a specific channel."""
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    await ctx.send(f'Message sent to {channel.name}')

@app.route('/notify', methods=['POST'])
def notify():
    item = request.json
    bot.loop.create_task(notify_discord(item))
    return 'Notification received', 200

async def notify_discord(item):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        title = item.get('title', 'No Title')
        description = item.get('description', 'No Description')
        price = item.get('price', 'No Price')
        original_price = item.get('articlesPrice', 'No Original Price')
        reason_discount = item.get('reasonDiscount', 'No Additional Note')
        hero_image = item.get('heroImage', '')

        embed = discord.Embed(
            title=f"**{title}**",
            url=f"https://www.ikea.com/hu/hu/this-is-ikea/sustainable-everyday/butormento-pont-pubd54f01d0#/{item.get('id')}",
            description=description
        )
        embed.add_field(name="Price", value=f"{price} Ft ~~{original_price} Ft~~", inline=False)
        embed.add_field(name="Additional note", value=reason_discount, inline=False)
        
        if hero_image:
            embed.set_image(url=hero_image)

        await channel.send(content="\n**New Entry Item listed:**", embed=embed)


async def request_task():
    while True:
        # Run request.py here
        await asyncio.create_subprocess_exec('python', './request.py')
        await asyncio.sleep(3 * 60 * 60)  # Sleep for 3 hours



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send('Ikea Scraper bot is started! Awaiting updates...')
    
    # Start the request task
    bot.loop.create_task(request_task())




# Start the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=4321)

# Run the Flask app in a separate thread
thread = threading.Thread(target=run_flask)
thread.start()

def signal_handler(sig, frame):
    print('Bot stopped')
    bot.loop.stop()
    thread.join()
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

bot.run(TOKEN)
