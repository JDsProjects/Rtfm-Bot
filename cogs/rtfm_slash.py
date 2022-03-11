import discord
from discord import app_commands
from discord.ext import commands


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="looks up docs")
    async def rtfm(interaction: discord.Interaction, library: str):
        await interaction.response.send_message(f"Alright Let's see {library}")

    @rtfm.autocomplete("library")
    async def rtfm_autocomplete(
        interaction: discord.Interaction, current: str, namespace: discord.AppCommandOptionType.string
    ):
        rtfm = interaction.client.rtfm_libraries

        return [
            app_commands.Choice(name=f"{library}", value=f"{rtfm.get(library)}")
            for library in rtfm
            if current.lower() in library.lower()
        ]


def setup(bot):
    bot.add_cog(test(bot))
