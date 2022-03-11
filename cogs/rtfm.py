from discord.ext import commands, menus
import discord, random
import utils
from discord.ext.menus.views import ViewMenuPages


class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def rtfm_lookup(self, program=None, *, args=None):
        cur = await self.bot.sus_users.cursor()
        cursor = await cur.execute("SELECT * FROM RTFM_DICTIONARY")
        rtfm_dictionary = dict(await cursor.fetchall())
        await cur.close()

        if not args:
            return rtfm_dictionary.get(program)

        else:
            url = rtfm_dictionary.get(program)

            results = await self.bot.scraper.search(args, page=url)

            if not results:
                return f"Could not find anything with {args}."

            else:
                return results

    async def rtfm_send(self, ctx, results):

        if isinstance(results, str):
            await ctx.send(results, allowed_mentions=discord.AllowedMentions.none())

        else:
            embed = discord.Embed(color=random.randint(0, 16777215))

            results = results[:10]
            embed.description = "\n".join(f"[`{result}`]({value})" for result, value in results)

            reference = utils.reference(ctx.message)
            await ctx.send(embed=embed, reference=reference)

    @commands.group(
        aliases=["rtd", "rtfs"],
        invoke_without_command=True,
        brief="most of this is based on R.danny including the reference(but this is my own code). But it's my own implentation of it",
    )
    async def rtfm(self, ctx, *, args=None):

        await ctx.trigger_typing()
        results = await self.rtfm_lookup(program="latest", args=args)
        await self.rtfm_send(ctx, results)

    class RtfmEmbed(menus.ListPageSource):
        async def format_page(self, menu, item):
            embed = discord.Embed(title="Packages:", description=item, color=random.randint(0, 16777215))
            return embed

    @commands.command(brief="a command to view the rtfm DB")
    async def rtfm_view(self, ctx):
        cur = await self.bot.sus_users.cursor()
        cursor = await cur.execute("SELECT * FROM RTFM_DICTIONARY")
        rtfm_dictionary = dict(await cursor.fetchall())
        await cur.close()

        pag = commands.Paginator()
        for g in rtfm_dictionary:
            pag.add_line(f"{g} : {rtfm_dictionary.get(g)}")
        pages = [page.strip("`") for page in pag.pages]

        menu = ViewMenuPages(self.RtfmEmbed(pages, per_page=1), delete_message_after=True)
        await menu.start(ctx)

    # from https://github.com/JDJGInc/JDBot/blob/master/cogs/info.py#L317


def setup(bot):
    bot.add_cog(DevTools(bot))
