from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional

from discord import app_commands
from discord.app_commands import Choice, Transform, Transformer
from discord.ext import commands

import utils
from utils import fuzzy
from utils.extra import RtfmObject

if TYPE_CHECKING:
    from discord import Interaction

    from main import RTFMBot
else:
    RTFMBot = commands.Bot


class LibraryTransformer(Transformer):
    async def transform(self, interaction: Interaction[RTFMBot], value: str) -> str:
        return interaction.client.rtfm_libraries.get(value, value)

    async def autocomplete(self, interaction: Interaction[RTFMBot], current: str) -> list[Choice]:
        choices = [Choice(name=name, value=name) for name in interaction.client.rtfm_libraries]
        start_with = list(filter(lambda x: x.name.startswith(current), choices)) or choices
        return start_with[:25]


class QueryTransformer(Transformer):
    async def transform(self, interaction: Interaction[RTFMBot], value: str) -> RtfmObject:
        library = interaction.client.rtfm_libraries.get(interaction.namespace.library, interaction.namespace.library)
        library = library or "https://discord.com/developers/docs/"
        unfiltered_results = await utils.rtfm(interaction.client, library)
        if item := fuzzy.find(value, unfiltered_results, key=lambda t: t.name):
            return item

        raise commands.BadArgument("No Results Found")

    async def autocomplete(self, interaction: Interaction[RTFMBot], current: str) -> list[Choice]:
        library = interaction.client.rtfm_libraries.get(interaction.namespace.library, interaction.namespace.library)
        library = library or "https://discord.com/developers/docs/"
        unfiltered_results = await utils.rtfm(interaction.client, library)
        choices = [
            Choice(name=result.name, value=result.name)
            for result in fuzzy.finder(current, unfiltered_results, key=lambda t: t.name)
        ]
        return choices[:25]


class DocsQueryTransformer(Transformer):
    async def transform(self, interaction: Interaction[RTFMBot], value: str) -> RtfmObject:
        unfiltered_results = await utils.algolia_lookup(
            interaction.client,
            os.environ["ALGOLIA_APP_ID"],
            os.environ["ALGOLIA_API_KEY"],
            "discord",
            value,
        )

        if result := fuzzy.find(value, unfiltered_results, key=lambda t: t.name):
            return result

        raise commands.BadArgument("No Results Found")

    async def autocomplete(self, interaction: Interaction[RTFMBot], current: str) -> list[Choice]:
        unfiltered_results = await utils.algolia_lookup(
            interaction.client,
            os.environ["ALGOLIA_APP_ID"],
            os.environ["ALGOLIA_API_KEY"],
            "discord",
            current,
        )
        # use new method to handle results from discord ologia, but fuzzy can be used now
        # I will remove the starting discord api docs if necessary.

        all_choices = [Choice(name=result.name, value=result.name) for result in unfiltered_results]

        if not current:
            return all_choices[:25]

        filtered_results = fuzzy.finder(current, unfiltered_results, key=lambda t: t.name)

        results = [Choice(name=result.name, value=result.name) for result in filtered_results]

        if not results:
            results = [Choice(name="Getting Started", value="Getting Started")]

        return results[:25]


Library = Transform[str, LibraryTransformer]
Query = Transform[RtfmObject, QueryTransformer]
DocsQuery = Transform[RtfmObject, DocsQueryTransformer]



class RTFMSlash(commands.Cog):
    def __init__(self, bot: RTFMBot) -> None:
        self.bot = bot

    @app_commands.command(name="rtfm")
    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    async def rtfm_slash(self, interaction: Interaction[RTFMBot], library: Library, query: Optional[Query]) -> None:
        """Looks up docs for a library with optionally a query.

        Parameters
        ----------
        library : str
            The library to search for.
        query : RtfmObject
            The query to search for.
        """
        url = query.url if query else library
        await interaction.response.send_message(f"Alright Let's see \n{url}")

    @rtfm_slash.error
    async def rtfm_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    @app_commands.command()
    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    async def docs(self, interaction: Interaction[RTFMBot], query: DocsQuery):
        """Looks up docs from discord developer docs with optionally a query.

        Parameters
        ----------
        query : RtfmObject
            The query to search for.
        """
        await interaction.response.send_message(f"Alright Let's see \n{query.url}")

    @docs.error
    async def docs_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(f"{error}! Please Send to this to my developer", ephemeral=True)
        print(error)
        print(interaction.command)

    @app_commands.command()
    @app_commands.user_install()
    @app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
    async def source(self, interaction: Interaction[RTFMBot]):
        """Sends link to the bot's source code"""
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label=f"Source",
                url="https://github.com/JDsProjects/Rtfm-Bot",
                style=discord.ButtonStyle.link,
            )
        )
        await interaction.response.send_message("Source: https://github.com/JDsProjects/Rtfm-Bot", view=view)

async def setup(bot: RTFMBot) -> None:
    await bot.add_cog(RTFMSlash(bot))
