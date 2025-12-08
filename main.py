# -------imports--------#
import os

from cyan_bot import CyanBot
from disnake.ext import commands
from disnake import Intents
from dotenv import load_dotenv

from db_db import PlayerDatabase


# Initialize the database
db = PlayerDatabase()

# gives the bot permissions to read messages
intents = Intents.default()
intents.message_content = True
intents.members = True
# sets up the bot object
bot = CyanBot(command_prefix="!", intents=intents, reload=True)
# Attach database to bot for access in cogs
bot.db = db


@bot.event
async def on_ready():
    # bot.add_cog(Roll(bot))
    # bot.add_cog(Admin(bot))
    # bot.add_cog(Activity(bot))
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

print("Loading extensions...")
bot.load_extension("commands.economy")
bot.load_extension("commands.admin")
bot.load_extension("commands.activity")
print("Loaded extensions.")

load_dotenv()
# runs the bot with the token
bot.run(os.getenv("BotTokenHere"))
