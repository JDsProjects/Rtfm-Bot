from discord.ext import commands, menus
from doc_search import AsyncScraper

class DevTools(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.loop.create_task(self.__ainit__())
  
  async def __ainit__(self):
    await self.bot.wait_until_ready()

    self.scraper = AsyncScraper(session = self.bot.session)

def setup(bot):
  bot.add_cog(DevTools(bot))