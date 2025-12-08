import random
import traceback

import disnake
from disnake import ui
from disnake import Embed
from disnake import Member
from disnake.ext import commands
from disnake.ext.commands import Bot, CommandError, Context, Cog


class betrollui(ui.View):
    def __init__(self, inter: disnake.ApplicationCommandInteraction, bet: int, luckyNumber: int, diceRange: int):
        super().__init__(timeout=180)
        self.initiator = inter.author
        self.bet = bet
        self.luckyNumber = luckyNumber
        self.diceRange = diceRange
        self.rolled = False
        self.result = None

        self.add_item(ui.Button(label=(f"Roll a D{self.diceRange} (Bet {self.bet})"), style=disnake.ButtonStyle.primary, custom_id="roll_main_dice"))
        @ui.Button(label=("Cancel Bet"),style=disnake.ButtonStyle.primary, custom_id="Cancel", row=1 )
        async def cancel_button()
class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_modified_users: list[int] = []

    def _push_modified_user(self, uid: int):
        if len(self._last_modified_users) == 10:
            self._last_modified_users.pop(0)
        self._last_modified_users.append(uid)

    # ----Payed roll command----#
    @commands.command(
        name="betroll",
        help="Roll a dice and bet on a lucky number! Usage: !betroll <bet amount> <lucky number> [range of dice, default 20]",
    )
    async def betroll(
        self,
        ctx: Context,
        bet: int,
        lucky_number: int,
        range: int = 20,
    ):
        user_id = ctx.author.id
        # ----Input validation----#
        if bet <= 0:
            return await ctx.send("Bet amount must be greater than zero.")
        if lucky_number < 1 or lucky_number > range:
            return await ctx.send(f"Your lucky number must be between 1 and {range}.")
        current_user = self.bot.db.fetch_user(user_id)
        if bet > current_user.balance:
            return await ctx.send(
                f"You do not have enough balance to place that bet. Your current balance is {current_user.balance}."
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
            new_balance = current_user.balance + Payout
            # ----Update balance----#
            current_user.balance = new_balance
            change_success = self.bot.db.update_user(current_user)

            if change_success:
                await ctx.send(
                    f"JACKPOT! You rolled a {result}! and won {Payout} coins! Your new balance is {new_balance}."
                )
            else:
                return await ctx.send("Error updating balance.")
        else:
            new_balance = current_user.balance - bet
            current_user.balance = new_balance
            change_success = self.bot.db.update_user(current_user)
            if change_success:
                await ctx.send(
                    f"You rolled a {result}. Sorry, you lost {bet} coins. Your new balance is {new_balance}."
                )
            else:
                return await ctx.send("Error updating balance.")

        self._push_modified_user(user_id)

    # ----betroll error handling----#
    @betroll.error  # type: ignore
    async def betroll_error(self: Cog, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number you wish to chose ex !roll 6.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid integer for the number.")
        else:
            await ctx.send("An error occurred while processing the command.")

    # ----Free roll command----#
    @commands.command()
    async def roll(self, ctx: Context, lucky_number: int, range: int = 20):
        await ctx.send(f"Lucky number {lucky_number}!")
        await ctx.reply(f"Rolling a D{range}...")
        result = random.randint(1, range)
        if result == lucky_number:
            await ctx.send(f"You rolled a {result}!")
        else:
            await ctx.send(f"Unlucky! You rolled a {result}.")

    # ----roll error handling----#
    @roll.error  # type: ignore
    async def roll_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the number you wish to chose ex !roll 6.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid integer for the number.")

    @commands.command(help="Gives or takes away money from a user.")
    @commands.has_permissions(administrator=True)
    async def fund(
        self, ctx: Context[commands.Bot], user_id: int | Member, amount: int
    ):
        if amount == 0:
            return await ctx.reply("Please specify an amount not equal to 0.")

        uid: int
        if isinstance(user_id, Member):
            uid = user_id.id
        elif isinstance(user_id, int):
            uid = user_id

        user = self.bot.db.fetch_user(uid)
        new_balance = user.balance + amount
        user.balance = new_balance
        success = self.bot.db.update_user(user)

        if not success:
            await ctx.send("Failed to fund user; no response from DB.")

        if amount > 0:
            await ctx.reply(f"Gave {amount} currency to <@{uid}>.")
        else:
            await ctx.reply(f"Yanked {amount} currency from <@{uid}>.")

        self._push_modified_user(uid)

    @fund.error
    async def fund_err(
        self: Cog,
        ctx: Context[commands.Bot],
        error: CommandError,
    ):
        traceback.print_exc()
        await ctx.send(f"Failed to fund user: {error}")
        raise Exception() from error

    @commands.command(help="Displays the bank accounts of the last 10 transactions.")
    @commands.has_permissions(administrator=True)
    async def funds(
        self,
        ctx: Context,
    ):
        users = self.bot.db.fetch_users(self._last_modified_users)

        if not users:
            return await ctx.reply(
                "No transactions have happened recently.", delete_after=10
            )

        ctext = "\n".join(f"{user.user_id} {user.balance}" for user in users)

        await ctx.reply(f"```\n{ctext}\n```", delete_after=20)

    @commands.command(help="Displays the balance of a user.")
    async def balance(self, ctx: Context, user_id: int | Member):
        uid: int
        if isinstance(user_id, Member):
            uid = user_id.id
        elif isinstance(user_id, int):
            uid = user_id

        user = self.bot.db.fetch_user(uid)

        await ctx.reply(f"<@{uid}>'s balance is {user.balance} coins.")
        

#teststuff
embededtest = Embed(

    title="Test",
    description="This is to test embededs", 
)




def setup(bot: Bot):
    bot.add_cog(economy(bot))
