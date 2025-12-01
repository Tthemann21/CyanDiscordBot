import time

from disnake import Member, Message
from disnake.ext import commands

from db_db import get_or_create_user, add_xp


class Activity(commands.Cog):
    """Activity Cog: awards XP for messages with a per-user cooldown to prevent spam.

    - Listens for member joins and ensures a DB row exists for the member.
    - Awards XP on messages but enforces an in-memory cooldown per user.
    """

    def __init__(self, bot):
        self.bot = bot
        # in-memory cooldown: user_id -> last_awarded_timestamp
        self._xp_cooldowns: dict[int, float] = {}
        # seconds between allowed XP awards per user
        self._xp_cooldown_seconds = 30
        # pruning: avoid letting the cooldown dict grow unbounded
        # we only prune periodically for efficiency
        self._last_prune: float = 0
        self._prune_interval_seconds: float = 300

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        user_id = member.id
        get_or_create_user(user_id)

    #async def level up_check(self, user_id: int, xp: int, level: int, ctx: commands.Context):
        # Placeholder for level check logic
        #if xp >= threshold:
            #level = level + 1


    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # ignore bot messages
        if message.author.bot:
            return

        user_id = message.author.id

        # ensure a DB row exists for this user
        # If the message is a valid command, don't award XP; let commands run
        ctx = await self.bot.get_context(message)
        if ctx.command is not None:
            #await self.bot.process_commands(message)
            return

        now = time.time()
        last_award = self._xp_cooldowns.get(user_id, 0)

        # Periodically prune expired entries to keep the dict small.
        # We do this only every `self._prune_interval_seconds` seconds
        # to avoid iterating too often when the bot is busy.
        if now - self._last_prune >= self._prune_interval_seconds:
            expired = [uid for uid, ts in self._xp_cooldowns.items() if now - ts >= self._xp_cooldown_seconds]
            for uid in expired:
                self._xp_cooldowns.pop(uid, None)
            self._last_prune = now

        if now - last_award < self._xp_cooldown_seconds:
            # still in cooldown window; don't award XP
            await self.bot.process_commands(message)
            return

        # Award XP and update last-award timestamp only if DB update succeeds
        xp_gained = 10
        # ensure the user exists in the DB only when we're about to award XP
        get_or_create_user(user_id)
        success = add_xp(user_id, xp_gained)
        if success:
            self._xp_cooldowns[user_id] = now

        # continue processing commands (if any)
        await self.bot.process_commands(message)

def setup(bot: commands.Bot):
    bot.add_cog(Activity(bot))
