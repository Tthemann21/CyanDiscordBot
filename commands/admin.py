from disnake import Member, TextChannel
from disnake.ext import commands
from disnake.ext.commands import Bot

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----purge command----#
    @commands.command(
        name="purge",
        help="Delete a number of messages from the channel. Usage: !purge <number>",
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context[Bot], number: int):
        if number <= 0:
            return await ctx.reply(
                "Number of messages to delete must be greater than zero."
            )
        channel = ctx.channel
        if not isinstance(channel, TextChannel):
            return await ctx.reply(
                "Purge can only be used in server text channels.", delete_after=10
            )

        await channel.purge(limit=number + 1)  # +1 to include the command message itself
        await ctx.send(f"Deleted {(number)} messages.", delete_after=5)

    # ----purge error handling----#
    @purge.error  # type: ignore
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
            guild_name = ctx.guild.name if ctx.guild is not None else "the server"
            await member.send(
                f"You have been kicked from {guild_name} for: {reason}"
            )
        except Exception as e:
            print(f"Error sending DM to {member.name}: {e}")

    # ----kick error handling----#
    @kick.error  # type: ignore
    async def kick_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please mention a valid user to kick.")
        else:
            await ctx.reply(
                "An error occurred while trying to execute the kick command."
            )

def setup(bot: Bot):
    bot.add_cog(Admin(bot))
