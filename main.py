# -------imports--------#
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

# gives the bot permissions to read messages
intents = discord.Intents.default()
intents.message_content = True

# sets up the bot object
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    # f string is good, prints into terminal when bot is online
    print(f"Booted up: {bot.user}")


# when I say !hello it says hello back
@bot.command()
# what is an async?
async def hello(ctx):
    # Ctx seems to be an input in chat, what is await?
    await ctx.send("Hello!")


@bot.command()
async def cmds(ctx):
    await ctx.send("Commands available: !hello, !roll <number>")


@bot.command()
async def roll(ctx, Lucky_number: int, Range: int = 20):
    await ctx.send(f"Lucky number {Lucky_number}!")
    await ctx.send(f"Rolling a D{Range}...")
    result = random.randint(1, Range)
    if result == Lucky_number:
        await ctx.send(f"You rolled a {result}!")
    else:
        await ctx.send(f"Unlucky! You rolled a {result}.")


@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the number you wish to chose ex !roll 6.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please enter a valid integer for the number.")


load_dotenv()
# runs the bot with the token
bot.run(os.getenv("BotTokenHere"))