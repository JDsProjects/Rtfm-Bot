from __future__ import annotations
from typing import TYPE_CHECKING
from discord import Object

from discord.ext import commands
import typing
from discord.app_commands import AppCommandError, command as app_command, Choice

if TYPE_CHECKING:
    from main import RTFMBot

    from discord import Interaction
else:
    RTFMBot = commands.Bot


class RTFMSlash(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    @app_command(description="looks up docs")
    async def rtfm(self, interaction: Interaction, library: str, query: typing.Optional[str] = None) -> None:
        """Looks up docs for a library with optionally a query."""
        if query is None:
            return await interaction.response.send_message(f"Alright Let's see {library}")

        await interaction.response.send_message(f"Alright Let's see {library}{query}")

    @rtfm.autocomplete("library")
    async def rtfm_library_autocomplete(self, interaction: Interaction, current: str) -> list[Choice]:
        libraries = self.bot.rtfm_libraries

        if not current:
            return [Choice(name=name, value=link) for name, link in libraries.items()][0:25]

        return [Choice(name=name, value=link) for name, link in libraries.items() if current.lower() in name.lower()][
            0:25
        ]

    @rtfm.autocomplete("query")
    async def rtfm_query_autocomplete(self, interaction: Interaction, current: str) -> list[Choice]:
        url = interaction.namespace.library or list(self.bot.rtfm_libraries.values())[0]

        assert self.bot.scraper is not None
        results = await self.bot.scraper.search(current, page=url)

        if not results or not current:
            results = ["Not Found", f"{current}."]
            return [Choice(name=item, value=item) for item in results]

        results = results[:25]
        return [Choice(name=name, value=link[len(url) :]) for name, link in results][0:25]

    @rtfm.error
    async def rtfm_error(self, interaction: Interaction, error: AppCommandError) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)


async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(RTFMSlash(bot), guild=Object(423828791098605578))
