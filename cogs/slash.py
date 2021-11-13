from discord.ext import commands, menus
from doc_search import AsyncScraper
import discord, random
import utils

class DevTools(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.loop.create_task(self.__ainit__())
  
  async def __ainit__(self):
    await self.bot.wait_until_ready()

    self.scraper = AsyncScraper(session = self.bot.session)
  
  async def rtfm_lookup(self, program = None, *, args = None):
    
    cur = await self.bot.sus_users.cursor()
    cursor=await cur.execute("SELECT * FROM RTFM_DICTIONARY")
    rtfm_dictionary = dict(await cursor.fetchall())
    await cur.close()

    if not args:
      return rtfm_dictionary.get(program)

    else:
      url = rtfm_dictionary.get(program)

      results = await self.scraper.search(args, page=url)

      if not results:
        return f"Could not find anything with {args}."

      else:
        return results

  async def rtfm_send(self, ctx, results):

    if isinstance(results, str):
      await ctx.send(results, allowed_mentions = discord.AllowedMentions.none())

    else: 
      embed = discord.Embed(color = random.randint(0, 16777215))

      results = results[:10]
      embed.description = "\n".join(f"[`{result}`]({value})" for result, value in results)

      reference = utils.reference(ctx.message)
      await ctx.send(embed=embed, reference = reference)

  @commands.group(aliases=["rtd", "rtfs"], invoke_without_command = True, brief="most of this is based on R.danny including the reference(but this is my own code). But it's my own implentation of it")
  async def rtfm(self, ctx, *, args = None):

    await ctx.trigger_typing()
    results = await self.rtfm_lookup(program="latest", args = args)
    await self.rtfm_send(ctx, results)

  

def setup(bot):
  bot.add_cog(DevTools(bot))