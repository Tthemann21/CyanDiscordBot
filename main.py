# -------imports--------#
import os

from disnake.ext import commands
from disnake import Intents
from dotenv import load_dotenv

from commands.roll import Roll
from commands.admin import Admin
from commands.activity import Activity
import db_db


db_db.database_setup()

# gives the bot permissions to read messages
intents = Intents.default()
intents.message_content = True
intents.members = True
# sets up the bot object
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(Roll(bot))

    await bot.add_cog(Admin(bot))

    await bot.add_cog(Activity(bot))
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


load_dotenv()
# runs the bot with the token
bot.run(os.getenv("BotTokenHere"))