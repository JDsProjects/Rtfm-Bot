from typing import TYPE_CHECKING

from discord import Guild
from discord.ext import commands

if TYPE_CHECKING:
    from main import RTFMBot
else:
    RTFMBot = commands.Bot


class Events(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(
            "Bot is Ready",
            f"Logged in as {self.bot.user} (ID: {self.bot.user.id})",  # type: ignore # .user isn't None.
            sep="\n",
        )

    @commands.Cog.listener()
    async def on_guild_available(self, guild: Guild) -> None:
        print(f"Guild {guild.name} (ID: {guild.id}) is available")

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild: Guild) -> None:
        print(f"Guild {guild.name} (ID: {guild.id}) is unavailable")


async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(Events(bot))
