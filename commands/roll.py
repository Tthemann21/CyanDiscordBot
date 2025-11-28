import random

from discord.ext import commands
from db_db import get_or_create_user, set_balance


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----Payed roll command----#
    @commands.command(
        name="Betroll",
        help="Roll a dice and bet on a lucky number! Usage: !betroll <bet amount> <lucky number> [range of dice, default 20]",
    )
    async def betroll(
        self, ctx: commands.Context, bet: int, lucky_number: int, range: int = 20
    ):
        user_id = ctx.author.id
        # ----Input validation----#
        if bet <= 0:
            return await ctx.send("Bet amount must be greater than zero.")
        if lucky_number < 1 or lucky_number > range:
            return await ctx.send(f"Your lucky number must be between 1 and {range}.")
        current_balance = get_or_create_user(user_id)
        if bet > current_balance:
            return await ctx.send(
                f"You do not have enough balance to place that bet. Your current balance is {current_balance}."
            )
        # ----Rolling the dice----#
        await ctx.reply(f"Rolling a D{range}...")
        await ctx.send(f"You bet {bet} coins on lucky number {lucky_number}.")

        result = random.randint(1, range)
        # ----Determining win/loss and updating balance----#
        if result == lucky_number:
            # ----Calculate payout----#
            Payoutfactor = range - 1
            Payout = bet * Payoutfactor
            new_balance = current_balance + Payout
            # ----Update balance----#
            change_success = set_balance(user_id, new_balance)

            if change_success:
                await ctx.send(
                    f"JACKPOT! You rolled a {result}! and won {Payout} coins! Your new balance is {new_balance}."
                )
            else:
                await ctx.send("Error updating balance.")
        else:
            new_balance = current_balance - bet
            change_success = set_balance(user_id, new_balance)
            if change_success:
                await ctx.send(
                    f"You rolled a {result}. Sorry, you lost {bet} coins. Your new balance is {new_balance}."
                )
            else:
                await ctx.send("Error updating balance.")

    # ----betroll error handling----#
    @betroll.error
    async def betroll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number you wish to chose ex !roll 6.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid integer for the number.")
        else:
            await ctx.send("An error occurred while processing the command.")

    # ----Free roll command----#
    @commands.command()
    async def roll(self, ctx: commands.Context, lucky_number: int, range: int = 20):
        await ctx.send(f"Lucky number {lucky_number}!")
        await ctx.reply(f"Rolling a D{range}...")
        result = random.randint(1, range)
        if result == lucky_number:
            await ctx.send(f"You rolled a {result}!")
        else:
            await ctx.send(f"Unlucky! You rolled a {result}.")

    # ----roll error handling----#
    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number you wish to chose ex !roll 6.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid integer for the number.")
