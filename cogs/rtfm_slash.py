from __future__ import annotations

import typing
from typing import TYPE_CHECKING
import os

from discord.app_commands import AppCommandError, Choice
from discord.app_commands import command as app_command
import discord
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

    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="looks up docs", name="rtfm")
    async def rtfm_slash(
        self, interaction: discord.Interaction, library: typing.Optional[str] = None, query: typing.Optional[str] = None
    ) -> None:
        """Looks up docs for a library with optionally a query."""

        library = library or self.bot.rtfm_libraries["master"]

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
        url = interaction.namespace.library or self.bot.rtfm_libraries["master"]
        unfiltered_results = await utils.rtfm(self.bot, url)

        all_choices = [Choice(name=result.name, value=result.url.removeprefix(url)) for result in unfiltered_results]

        if not current:
            return all_choices[:25]

        filtered_results = fuzzy.finder(current, unfiltered_results, key=lambda t: t[0])

        results = [Choice(name=result.name, value=result.url.removeprefix(url)) for result in filtered_results]

        return results[:25]

    @rtfm_slash.error
    async def rtfm_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="looks up docs from discord developer docs", name="docs")
    async def docs(
        self, interaction: discord.Interaction, query: typing.Optional[str] = None
    ) -> None:
        """Looks up docs from discord developer docs with optionally a query."""

        url = "https://discord.com/developers/docs/"
        if query is None or query == "No Results Found":
            # place holder for now.
            return await interaction.response.send_message(f"Alright Let's see \n{url}")

        await interaction.response.send_message(f"Alright Let's see \n{url+query}")

    @docs.autocomplete("query")
    async def docs_autocomplete(self, interaction: discord.Interaction, current: str) -> list[Choice]:

        url = "https://discord.com/developers/docs/"

        unfiltered_results = await utils.algolia_lookup(self.bot, os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_API_KEY"], "discord", current)
        # use new method to handle results from discord ologia, but fuzzy can be used now
        # I will remove the starting discord api docs if necessary.

        all_choices = [Choice(name=result.name, value=result.url.removeprefix(url)) for result in unfiltered_results]

        if not current:
            return all_choices[:25]

        filtered_results = fuzzy.finder(current, unfiltered_results, key=lambda t: t[0])

        results = [Choice(name=result.name, value=result.url.removeprefix(url)) for result in filtered_results]

        for result in results:
            if len(result.value) > 100:
                print(result.value)

         # seems to have issues with some sizes.

        if not results:
            result = utils.RtfmObject("Getting Started", "https://discord.com/developers/docs/")
            results = [Choice(name=result.name, value=result.url.removeprefix(url))]

        return results[:25]

    @docs.error
    async def docs_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="sends link to bot's source code", name="source")
    async def source(self, interaction: discord.Interaction):

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label=f"Source",
                url="https://github.com/JDsProjects/Rtfm-Bot",
                style=discord.ButtonStyle.link,
            )
        )
        await interaction.response.send_message(
            "Source: https://github.com/JDsProjects/Rtfm-Bot", view=view
        )

async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(RTFMSlash(bot))
