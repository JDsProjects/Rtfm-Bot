import discord
from discord import app_commands
from discord.ext import commands


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(self.rtfm._params)

    @app_commands.command(description="looks up docs")
    async def rtfm(self, interaction: discord.Interaction, library: str):
        await interaction.response.send_message(f"Alright Let's see {library}")


def setup(bot):
    bot.add_cog(test(bot))
