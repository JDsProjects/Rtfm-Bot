from discord.ext import commands
import discord, random, os


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Ready")
        print(f"Logged in as {self.bot.user}")
        print(f"Id: {self.bot.user.id}")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        print(f"{guild} is avaible")

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild):
        print(f"{guild} is unavaible")


async def setup(bot):
    await bot.add_cog(Events(bot))
