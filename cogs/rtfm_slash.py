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

        await interaction.response.send_message(f"Alright Let's see {library}{query}")

    @rtfm.autocomplete("library")
    async def rtfm_autocomplete(self, interaction: discord.Interaction, current: str):
        namespace = interaction.namespace
        rtfm = interaction.client.rtfm_libraries

        return [
            app_commands.Choice(name=f"{library}", value=f"{rtfm.get(library)}")
            for library in rtfm
            if current.lower() in library.lower()
        ]
        # if someone wants to attempt to support more than 25 libraries, this is where it would go, anyways.
        # I think if someone really wants to do this, show up the first 25 libraries, if lookup show more up to 25 libraries.

    @rtfm.autocomplete("query")
    async def rtfm_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        namespace = interaction.namespace
        default = list(interaction.client.rtfm_libraries.values())[0]
        url = namespace.library or default

        results = await self.bot.scraper.search(f"{current}", page=f"{url}")

        if not results:
            results = {"Not Found", f"{current}."}

        results = results[:25]
        results = dict(results)
        cut_off = len(url)
        return [app_commands.Choice(name=f"{result}", value=f"{results.get(result)[cut_off:]}") for result in results]

    @rtfm.error
    async def rtfm_error(self, interaction: discord.Interaction, command, error):
        print(error)
        print(command)


async def setup(bot):
    await bot.add_cog(test(bot))
