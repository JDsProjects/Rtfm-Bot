import discord
from discord import app_commands
from discord.ext import commands
import typing


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="looks up docs")
    async def rtfm(self, interaction: discord.Interaction, library: str, query: typing.Optional[str] = None):

        if query is None:
            return await interaction.response.send_message(f"Alright Let's see {library}")

        await interaction.response.send_message(f"Alright Let's see {query}")

    @rtfm.autocomplete("library")
    async def rtfm_autocomplete(
        self, interaction: discord.Interaction, current: str, namespace: discord.AppCommandOptionType.string
    ):
        rtfm = interaction.client.rtfm_libraries

        return [
            app_commands.Choice(name=f"{library}", value=f"{rtfm.get(library)}")
            for library in rtfm
            if current.lower() in library.lower()
        ]

    @rtfm.autocomplete("query")
    async def rtfm_autocomplete(
        self, interaction: discord.Interaction, current: str, namespace: discord.AppCommandOptionType.string
    ):
        default = list(interaction.client.rtfm_libraries.values())[0]
        print(default)
        url = namespace.__dict__.get("library", default)

        results = await self.bot.scraper.search(f"{current}", page=f"{url}")
        print(type(results))

        if not results:
            results = {"Not Found", f"{current}."}

        # results = results[:25]
        results = results[:10]
        results = dict(results)
        print([app_commands.Choice(name=f"{result.lstrip(url)}", value=f"{results.get(result)}") for result in results])

        return [app_commands.Choice(name=f"{result}", value=f"{results.get(result)}") for result in results]

    @rtfm.error
    async def rtfm_error(self, interaction: discord.Interaction, command, error):
        print(error)
        print(command)


def setup(bot):
    bot.add_cog(test(bot))
