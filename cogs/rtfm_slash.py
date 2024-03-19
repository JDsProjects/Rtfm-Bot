from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from discord.app_commands import AppCommandError, Choice
from discord.app_commands import command as app_command
from discord.ext import commands
from discord import app_commands
from utils import fuzzy
import utils

if TYPE_CHECKING:
    from discord import Interaction

    from main import RTFMBot
else:
    RTFMBot = commands.Bot


class RTFMSlash(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    @app_commands.command(description="looks up docs", name="rtfm")
    async def rtfm_slash(
        self, interaction: discord.Interaction, library: str, query: typing.Optional[str] = None
    ) -> None:
        """Looks up docs for a library with optionally a query."""
        if query is None or query == "No Results Found":
            return await interaction.response.send_message(f"Alright Let's see \n{library}")

        await interaction.response.send_message(f"Alright Let's see \n{library+query}")

    @rtfm_slash.autocomplete("library")
    async def rtfm_library_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:
        libraries = self.bot.rtfm_libraries

        all_choices: list[Choice] = [Choice(name=name, value=link) for name, link in libraries.items()]
        startswith: list[Choice] = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @rtfm_slash.autocomplete("query")
    async def rtfm_query_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:
        url = interaction.namespace.library or list(dict(self.rtfm_dictionary).values())[0]
        unfiltered_results = await utils.rtfm(self.bot, url)

        all_choices = [Choice(name=result.name, value=result.url.replace(url, "")) for result in unfiltered_results]

        if not current:
            return all_choices[:25]

        filtered_results = fuzzy.finder(current, unfiltered_results, key=lambda t: t[0])

        results = [Choice(name=result.name, value=result.url.replace(url, "")) for result in filtered_results]

        return results[:25]

    @rtfm_slash.error
    async def rtfm_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    @app_commands.private_channel_only()
    @app_commands.command(description="looks up docs but for dms and group chats", name="rtfm-private")
    async def rtfm_slash_private(
        self, interaction: discord.Interaction, library: str, query: typing.Optional[str] = None
    ) -> None:
        """Looks up docs for a library with optionally a query."""
        if query is None or query == "No Results Found":
            return await interaction.response.send_message(f"Alright Let's see \n{library}")

        await interaction.response.send_message(f"Alright Let's see \n{library+query}")

    @rtfm_slash_private.autocomplete("library")
    async def rtfm_library_private_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:
        libraries = self.bot.rtfm_libraries

        all_choices: list[Choice] = [Choice(name=name, value=link) for name, link in libraries.items()]
        startswith: list[Choice] = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @rtfm_slash_private.autocomplete("query")
    async def rtfm_query_private_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:
        url = interaction.namespace.library or list(dict(self.rtfm_dictionary).values())[0]
        unfiltered_results = await utils.rtfm(self.bot, url)

        all_choices = [Choice(name=result.name, value=result.url.replace(url, "")) for result in unfiltered_results]

        if not current:
            return all_choices[:25]

        filtered_results = fuzzy.finder(current, unfiltered_results, key=lambda t: t[0])

        results = [Choice(name=result.name, value=result.url.replace(url, "")) for result in filtered_results]

        return results[:25]

    @rtfm_slash_private.error
    async def rtfm_private_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    
    @app_commands.dm_only()
    @app_commands.command(description="looks up docs but for dms and group chats", name="test")
    async def test(
        self, interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message("Testing This.")

async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(RTFMSlash(bot))
