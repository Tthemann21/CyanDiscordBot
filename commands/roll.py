import random

from discord.ext import commands


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, lucky_number: int, range: int = 20):
        await ctx.send(f"Lucky number {lucky_number}!")
        await ctx.send(f"Rolling a D{range}...")
        result = random.randint(1, range)
        if result == lucky_number:
            await ctx.send(f"You rolled a {result}!")
        else:
            await ctx.send(f"Unlucky! You rolled a {result}.")

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number you wish to chose ex !roll 6.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid integer for the number.")
