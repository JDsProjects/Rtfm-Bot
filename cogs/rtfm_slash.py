from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from discord.app_commands import AppCommandError, Choice
from discord.app_commands import command as app_command
from discord.ext import commands

if TYPE_CHECKING:
    from discord import Interaction

    from main import RTFMBot
else:
    RTFMBot = commands.Bot


class RTFMSlash(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    @app_command(description="looks up docs")
    async def rtfm(self, interaction: Interaction, library: str, query: typing.Optional[str] = None) -> None:
        """Looks up docs for a library with optionally a query."""
        if query is None or query == "No Results Found":
            return await interaction.response.send_message(f"Alright Let's see {library}")

        await interaction.response.send_message(f"Alright Let's see {library}{query}")

    @rtfm.autocomplete("library")
    async def rtfm_library_autocomplete(self, interaction: Interaction, current: str) -> list[Choice]:
        libraries = self.bot.rtfm_libraries

        all_choices: list[Choice] = [Choice(name=name, value=link) for name, link in libraries.items()]
        startswith: list[Choice] = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith

    @rtfm.autocomplete("query")
    async def rtfm_query_autocomplete(self, interaction: Interaction, current: str) -> list[Choice]:
        url = interaction.namespace.library or list(self.bot.rtfm_libraries.values())[0]

        assert self.bot.scraper is not None
        results = await self.bot.scraper.search(current, page=url)

        if not results:
            return [Choice(name="No results found", value="No Results Found")]

        to_slice_link = len(url)
        all_choices: list[Choice] = [Choice(name=name, value=link[to_slice_link:]) for name, link in results]
        startswith: list[Choice] = [choices for choices in all_choices if choices.name.startswith(current)]
        if not current:
            return all_choices[:25]

        return startswith[:25]

    @rtfm.error
    async def rtfm_error(self, interaction: Interaction, error: AppCommandError) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)


async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(RTFMSlash(bot))
