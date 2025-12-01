from disnake.ext import commands
from disnake import Member

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----purge command----#
    @commands.command(
        name="purge",
        help="Delete a number of messages from the channel. Usage: !purge <number>",
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, number: int):
        if number <= 0:
            return await ctx.reply(
                "Number of messages to delete must be greater than zero."
            )

        await ctx.channel.purge(
            limit=number + 1
        )  # +1 to include the command message itself
        await ctx.send(f"Deleted {(number)} messages.", delete_after=5)

    # ----purge error handling----#
    @purge.error
    async def purge_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid number of messages to delete.")
        else:
            await ctx.reply(
                "An error occurred while trying to execute the purge command."
            )

    # ----kick command----#
    @commands.command(
        name="kick", help="Kick a user from the server. Usage: !kick <user>"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: Member, *, reason=None):
        await member.kick(reason=reason)

        if reason:
            await ctx.reply(
                f"{member.mention} was kicked for: **{reason}**", mention_author=False
            )
        try:
            await member.send(
                f"You have been kicked from {ctx.guild.name} for: {reason}"
            )
        except Exception as e:
            print(f"Error sending DM to {member.name}: {e}")

    # ----kick error handling----#
    @kick.error
    async def kick_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please mention a valid user to kick.")
        else:
            await ctx.reply(
                "An error occurred while trying to execute the kick command."
            )
