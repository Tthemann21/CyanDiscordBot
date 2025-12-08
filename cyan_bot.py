from disnake.ext.commands import Bot

from db_db import PlayerDatabase


class CyanBot(Bot):
    """Custom Bot subclass with typed database attribute."""
    db: PlayerDatabase

    async def close(self) -> None:
        """Close the bot and ensure the attached database is closed.

        This overrides the base close to always attempt to close `self.db`.
        """
        try:
            await super().close()
        finally:
            try:
                if hasattr(self, "db") and self.db is not None:
                    self.db.close()
            except Exception:
                pass

